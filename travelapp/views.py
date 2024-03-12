from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User 
from travelapp.forms import *
from .models import *
from django.views.generic import ListView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import redirect
from .forms import LoginForm
from django.views.generic import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.urls import reverse

from django.contrib import messages
from urllib.parse import urlparse, urlunparse

from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
	REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
	logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
	AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
	url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from datetime import date
from django.conf import settings
from django.core.mail import send_mail
import math, random
import os
from django.views import View
from django.db import transaction
from decimal import Decimal

''' Authentication'''

class SuperUserMixin(object):
	""" A mixin requiring a user to be logged in. """
	def dispatch(self, request, *args, **kwargs):

		if not request.user.is_authenticated:
			return redirect('/travelapp/login/')
		return super(SuperUserMixin, self).dispatch(request, *args, **kwargs)

class SuccessURLAllowedHostsMixin:
	success_url_allowed_hosts = set()

	def get_success_url_allowed_hosts(self):
		return {self.request.get_host(), *self.success_url_allowed_hosts}

class LoginView(SuccessURLAllowedHostsMixin, FormView):
	"""
	Display the login form and handle the login action.
	"""
	form_class = AuthenticationForm
	authentication_form = None
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'user_login.html'
	redirect_authenticated_user = False
	extra_context = None

	@method_decorator(sensitive_post_parameters())
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		if self.redirect_authenticated_user and self.request.user.is_authenticated:
			redirect_to = self.get_success_url()
			if redirect_to == self.request.path:
				raise ValueError(
					"Redirection loop for authenticated user detected. Check that "
					"your LOGIN_REDIRECT_URL doesn't point to a login page."
				)
			return HttpResponseRedirect(redirect_to)
		return super().dispatch(request, *args, **kwargs)

	def get_success_url(self):
		url = self.get_redirect_url()
		return url or resolve_url('index')

	def get_redirect_url(self):
		"""Return the user-originating redirect URL if it's safe."""
		redirect_to = self.request.POST.get(
			self.redirect_field_name,
			self.request.GET.get(self.redirect_field_name, '')
		)
		url_is_safe = url_has_allowed_host_and_scheme(
			url=redirect_to,
			allowed_hosts=self.get_success_url_allowed_hosts(),
			require_https=self.request.is_secure(),
		)
		return redirect_to if url_is_safe else ''

	def get_form_class(self):
		return self.authentication_form or self.form_class

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

	def form_valid(self, form):
		"""Security check complete. Log the user in."""
		auth_login(self.request, form.get_user())
		return HttpResponseRedirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_site = get_current_site(self.request)
		context.update({
			self.redirect_field_name: self.get_redirect_url(),
			'site': current_site,
			'site_name': current_site.name,
			**(self.extra_context or {})
		})
		return context	

		

class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
	"""
	Log out the user and display the 'You are logged out' message.
	"""
	next_page = None
	redirect_field_name = REDIRECT_FIELD_NAME
	template_name = 'index.html'
	extra_context = None

	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		auth_logout(request)
		next_page = self.get_next_page()
		if next_page:
			# Redirect to this page until the session has been cleared.
			return HttpResponseRedirect(next_page)
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		"""Logout may be done via POST."""
		return self.get(request, *args, **kwargs)

	def get_next_page(self):
		if self.next_page is not None:
			next_page = resolve_url(self.next_page)
		elif settings.LOGOUT_REDIRECT_URL:
			next_page = resolve_url('user_login')
		else:
			next_page = self.next_page

		if (self.redirect_field_name in self.request.POST or
				self.redirect_field_name in self.request.GET):
			next_page = self.request.POST.get(
				self.redirect_field_name,
				self.request.GET.get(self.redirect_field_name)
			)
			url_is_safe = url_has_allowed_host_and_scheme(
				url=next_page,
				allowed_hosts=self.get_success_url_allowed_hosts(),
				require_https=self.request.is_secure(),
			)
			# Security check -- Ensure the user-originating redirection URL is
			# safe.
			if not url_is_safe:
				next_page = self.request.path
		return next_page

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		current_site = get_current_site(self.request)
		context.update({
			'site': current_site,
			'site_name': current_site.name,
			'title': _('Logged out'),
			**(self.extra_context or {})
		})
		return context


def logout_then_login(request, login_url=None):
	"""
	Log out the user if they are logged in. Then redirect to the login page.
	"""
	login_url = resolve_url('user_login')
	return LogoutView.as_view(next_page=login_url)(request)


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
	"""
	Redirect the user to the login page, passing the given 'next' page.
	"""
	resolved_url = resolve_url(login_url or settings.LOGIN_URL)

	login_url_parts = list(urlparse(resolved_url))
	if redirect_field_name:
		querystring = QueryDict(login_url_parts[4], mutable=True)
		querystring[redirect_field_name] = next
		login_url_parts[4] = querystring.urlencode(safe='/')

	return HttpResponseRedirect(urlunparse(login_url_parts))


class SignupView(SuccessMessageMixin, FormView, SignupForm):
	"""Signup View."""
	model = CustomUser
	template_name = 'signup.html'
	form_class = SignupForm
	success_url = reverse_lazy('user_login')
	success_message = "Registration Successfully"

	def form_valid(self, form):
		"""If the form is valid save the user"""
		form.save()
		return super().form_valid(form) 

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

class HomeView(TemplateView):
	template_name='index.html' 



class UpcomingTripsView(SuperUserMixin, ListView):
	model = Package
	template_name = 'manage_upcomingtrips.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		object_list = Package.objects.filter(pstatus=1)
		return object_list  

	def get_context_data(self, *args, **kwargs):
		try:
			return super(UpcomingTripsView, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(UpcomingTripsView, self).get_context_data(*args, **kwargs)
			

# Trips detials view
class TripDetailsView(SuperUserMixin, ListView):
	model = Package
	template_name = 'trip_details.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		object_list = Package.objects.filter(slug=self.kwargs['slug'],pstatus=1).select_related() 
		return object_list

	def get_context_data(self, *args, **kwargs):
		try:
			return super(TripDetailsView, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(TripDetailsView, self).get_context_data(*args, **kwargs)


# Trips detials view
class BookTripView(SuperUserMixin ,ListView):
	model = Package
	template_name = 'booktrip.html'
	
	def get_queryset(self, *args, **kwargs):
		object_list = Package.objects.filter(slug=self.kwargs['slug'],pstatus=1).select_related() 
		return object_list


class CreateTrip(SuperUserMixin, SuccessMessageMixin, CreateView):

	def post(self, request, *args, **kwargs):

		if request.method == 'POST':
			uniqueslug = request.POST.get('uniqueslug')
			trip_object = Package.objects.get(slug=uniqueslug)
			paid = request.POST.get('paidamount')
			totalprice = request.POST.get('totalprice')
			outstanding = Decimal(totalprice) - Decimal(paid)

			with transaction.atomic():
				tripreservation = Booking(
					pid = trip_object,
					bcname = request.POST.get('fullname'),
					bfrom_date = request.POST.get('from_date'),
					bto_date = request.POST.get('to_date'),
					btripprice = request.POST.get('tripprice'),
					bremaining_amount=outstanding,
					bperson = request.POST.get('person'),
					btotalprice = request.POST.get('totalprice'),
					bchildren = request.POST.get('children'),
					cid = self.request.user
				)
				tripreservation.save()
				

				reservationpayment = RemaningReservationPayment(
					trip_id=trip_object,
					paid_amount=paid,
					paymentmethod = request.POST.get('paymentMethod'),
					reg_user = self.request.user
				)
				reservationpayment.save()

				messages.success(self.request, 'Trip reservation successfully.')
				return redirect('/travelapp/showTrips')
		else:
			raise Http404("Faild.")	


class ShowTripView(SuperUserMixin, ListView):
	model = Booking
	template_name = 'showtrip.html'

	def get_queryset(self, *args, **kwargs):
		object_list = Booking.objects.filter(bstatus=1, cid = self.request.user).select_related()
		return object_list  

	def get_context_data(self, **kwargs):
		context = super(ShowTripView, self).get_context_data(**kwargs)
		context['tripreservation'] = Booking.objects.filter(bstatus=1, cid = self.request.user).select_related()
		context['reservationpayment'] = RemaningReservationPayment.objects.filter(status=1, reg_user=self.request.user).select_related()
		return context	

