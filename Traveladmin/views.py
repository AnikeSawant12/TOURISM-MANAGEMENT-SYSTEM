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
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User 
from django.http import Http404, JsonResponse, HttpResponseRedirect, HttpResponse
from travelapp .models import *
from travelapp .forms import *
from django.contrib.messages.views import SuccessMessageMixin
from io import BytesIO 
from django.template.loader import get_template
from django.views.generic import View
from xhtml2pdf import pisa 
from django.db.models import Q, F
from datetime import date
import csv
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from django.contrib import messages
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from decimal import Decimal


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
 
	#This part will create the pdf.
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

# Authentication
class SuperUserMixin(object):
	""" A mixin requiring a user to be super user """

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('/TravelAdmin/login')				
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
	template_name = 'login.html'
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
		return url or resolve_url('dashboard')

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
	template_name = 'logout.html'
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
			next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
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
	login_url = resolve_url(login_url or settings.LOGIN_URL)
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

# End Authentication

# Show Dashboard
class DashboardView(SuperUserMixin, TemplateView):
	template_name='dashboard.html' 



# manage hotel
class ManageHotelView(SuperUserMixin, ListView):
	model = Services
	template_name = 'manage_hotels.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		name = self.request.GET.get('q')
		object_list = Services.objects.filter(sstatus=1)
		if name:
			object_list = object_list.filter(shotelname__icontains=name)
		return object_list  


	def get_context_data(self, *args, **kwargs):
		try:
			return super(ManageHotelView, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(ManageHotelView, self).get_context_data(*args, **kwargs)


class CreateNewHotelView(SuperUserMixin, SuccessMessageMixin, CreateView):
	model = Services
	template_name = 'add_hotel.html'
	form_class = HotelForm 
	success_url = reverse_lazy('manageHotel')
	success_message = "The Hotel %(shotelname)s Was Created Successfully"

	def form_valid(self,form):
		form.instance.screated_by = self.request.user
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))			


class EditHotelview(SuperUserMixin, SuccessMessageMixin, UpdateView):
	model = Services
	template_name = 'edit_hotel.html'
	form_class = HotelForm
	success_url = reverse_lazy('manageHotel')
	success_message = "The Hotel %(shotelname)s Was Updated Successfully" 

	def form_valid(self,form):
		form.instance.created_by = self.request.user
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))		


class DeleteHotelView(SuperUserMixin, SuccessMessageMixin, RedirectView):
	url = '/Traveladmin/manageHotel'

	def get_redirect_url(self, *args, **kwargs):
		del_id = kwargs['slug']
		Services.objects.filter(slug=del_id).update(sstatus=2)
		return super().get_redirect_url(*args, **kwargs)		


# manage Trips
class ManageTrips(SuperUserMixin, SuccessMessageMixin, ListView):
	model = Package
	template_name = 'manage_trips.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		name = self.request.GET.get('q')
		object_list = Package.objects.filter(pstatus=1)
		if name:
			object_list = object_list.filter(plocation__icontains=name)
		return object_list  


	def get_context_data(self, *args, **kwargs):
		try:
			return super(ManageTrips, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(ManageTrips, self).get_context_data(*args, **kwargs)


class CreateTripView(SuperUserMixin, SuccessMessageMixin, CreateView):
	model = Package
	template_name = 'add_trips.html'
	form_class = TripsFrom 
	success_url = reverse_lazy('manageUpcomingtrips')
	success_message = "The Trip %(plocation)s Was Created Successfully"

	def form_valid(self,form):
		form.instance.pcreated_by = self.request.user
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

class EditTripView(SuperUserMixin, SuccessMessageMixin, UpdateView):
	model = Package
	template_name = 'edit_trip.html'
	form_class = TripsFrom
	success_url = reverse_lazy('manageUpcomingtrips')
	success_message = "The Trip %(plocation)s Was Updated Successfully" 

	def form_valid(self,form):
		form.instance.pcreated_by = self.request.user
		form.save()
		return super().form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

# Trips detials view
class TripDetailsView(SuperUserMixin, SuccessMessageMixin, ListView):
	model = Package
	template_name = 'trips_details.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		name = self.request.GET.get('q')
		object_list = Package.objects.filter(slug=self.kwargs['slug'],pstatus=1).select_related()
		return object_list  


	def get_context_data(self, *args, **kwargs):
		try:
			return super(TripDetailsView, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(TripDetailsView, self).get_context_data(*args, **kwargs)		


class DeleteTripView(SuperUserMixin, SuccessMessageMixin, RedirectView):
	url = '/Traveladmin/manageUpcomingtrips'

	def get_redirect_url(self, *args, **kwargs):
		del_id = kwargs['slug']
		Package.objects.filter(slug=del_id).update(status=2)
		return super().get_redirect_url(*args, **kwargs)


class ViewNewTripsView(SuperUserMixin, ListView):
	model = Booking
	template_name = 'view_trips_details.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		object_list = Booking.objects.filter(bstatus=1, btrip_status=1).select_related()
		return object_list  


	def get_context_data(self, *args, **kwargs):
		try:
			return super(ViewNewTripsView, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(ViewNewTripsView, self).get_context_data(*args, **kwargs)


class TripProcessView(SuperUserMixin ,RedirectView):
	url = '/Traveladmin/viewNewtrips'

	def get_redirect_url(self, *args, **kwargs):
		process_slug = kwargs['slug']
		Booking.objects.filter(slug=process_slug).update(btrip_status=2)
		return super().get_redirect_url(*args, **kwargs) 


class InProcessTrips(SuperUserMixin, ListView):
	model = Booking
	template_name = 'inprocess_trips.html'
	ordering = ['-id']
	paginate_by = 10
	paginate_orphans = 1

	def get_queryset(self, *args, **kwargs):
		object_list = Booking.objects.filter(bstatus=1, btrip_status=2).select_related()
		return object_list  


	def get_context_data(self, *args, **kwargs):
		try:
			return super(InProcessTrips, self).get_context_data(*args, **kwargs)
		except Http404:
			self.kwargs['page'] = 1
			return super(InProcessTrips, self).get_context_data(*args, **kwargs)