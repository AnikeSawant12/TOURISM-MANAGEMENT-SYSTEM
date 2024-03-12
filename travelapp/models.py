from __future__ import unicode_literals
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.db import models
from .slug import *
from django.db.models.signals import pre_save
from datetime import date, timedelta


class CustomUser(AbstractBaseUser, PermissionsMixin):
	GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

	cusername = models.CharField(_('cusername'), max_length=10, unique=True)
	cemail = models.EmailField(_('cemail address'), unique=True)
	cfname = models.CharField(_('cfname'), max_length=200, null=True)
	cmname = models.CharField(max_length=20, null=True)
	clname = models.CharField(max_length=20, null=True)
	cgender = models.CharField(max_length=10, choices=GENDER_CHOICES)
	cmobileno = models.CharField(max_length=50, null=True)
	caddress1 = models.CharField(max_length=20, null=True)
	caddress2 = models.CharField(max_length=20, null=True)
	ccity = models.CharField(max_length=20, null=True)
	cstate = models.CharField(max_length=20, null=True)
	ccountry = models.CharField(max_length=20, null=True)
	cpin = models.CharField(max_length=20, null=True)
	slug = models.SlugField(unique=True, null=True, blank=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)

	USERNAME_FIELD = 'cusername'
	REQUIRED_FIELDS = ['cemail']

	objects = CustomUserManager()

	def __str__(self):
		return self.cusername

def pre_save_user_name(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator_user_name(instance)

pre_save.connect(pre_save_user_name, sender = CustomUser)


class Services(models.Model):
	shotelname = models.CharField(max_length=100, unique=True, null=True)
	shotelimg = models.ImageField(upload_to='images/', null=True)
	shoteltype = models.CharField(max_length=100, null=True)
	sdesc = models.CharField(max_length=600, null=True)
	sstatus = models.IntegerField(default=1,null=True)
	slug = models.SlugField(unique=True, null=True, blank=True)
	screated_at = models.DateTimeField(auto_now_add=True)
	supdated_at = models.DateTimeField(auto_now=True)
	screated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.shotelname

def pre_save_hotel(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator_hotel(instance)

pre_save.connect(pre_save_hotel, sender = Services)		


class Package(models.Model):
	plocation = models.CharField(max_length=100, null=True, unique=True)
	pdays = models.IntegerField(null=True)
	pnights = models.IntegerField(null=True)
	pprice = models.FloatField(null=True)
	plocationimg = models.ImageField(upload_to='images/', blank=True)
	photel = models.ForeignKey(Services, on_delete=models.CASCADE)
	pfrom_date = models.DateField(null=True)
	pto_date = models.DateField(null=True)
	pday1 = models.CharField(max_length=200, null=True)
	pday1_desc = models.CharField(max_length=1000, null=True)
	pday2 = models.CharField(max_length=200, null=True)
	pday2_desc = models.CharField(max_length=1000, null=True)
	pday3 = models.CharField(max_length=200, null=True)
	pday3_desc = models.CharField(max_length=1000, null=True)
	pday4 = models.CharField(max_length=200, null=True)
	pday4_desc = models.CharField(max_length=1000, null=True)
	pday5 = models.CharField(max_length=200, null=True)
	pday5_desc = models.CharField(max_length=1000, null=True)
	pday6 = models.CharField(max_length=200, null=True)
	pday6_desc = models.CharField(max_length=1000, null=True)
	pstatus = models.IntegerField(default=1,null=True)
	slug = models.SlugField(unique=True, null=True, blank=True)
	pcreated_at = models.DateTimeField(auto_now_add=True)
	pupdated_at = models.DateTimeField(auto_now=True)
	pcreated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


def pre_save_trips(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator_trips(instance)

pre_save.connect(pre_save_trips, sender = Package)



class Booking(models.Model):
	pid = models.ForeignKey(Package, on_delete=models.CASCADE)
	bcname = models.CharField(max_length=100, null=True)
	bfrom_date = models.DateField(null=True)
	bto_date = models.DateField(null=True)
	btripprice = models.FloatField(null=True)
	bperson = models.IntegerField(null=True)
	btotalprice = models.FloatField(null=True)
	bremaining_amount = models.IntegerField(null=True)
	bchildren = models.IntegerField(null=True)
	btrip_status = models.IntegerField(default=1, null=True)
	bstatus = models.IntegerField(default=1,null=True)
	slug = models.SlugField(unique=True, null=True, blank=True)
	bcreated_at = models.DateTimeField(auto_now_add=True)
	bupdated_at = models.DateTimeField(auto_now=True)
	cid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


	
def pre_save_trip_reservation(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = unique_slug_generator_trips_reservation(instance)

pre_save.connect(pre_save_trip_reservation, sender = Booking)


class RemaningReservationPayment(models.Model):
	trip_id = models.ForeignKey(Package, on_delete=models.CASCADE)
	paid_amount = models.IntegerField(null=True)
	paymentmethod = models.CharField(max_length=100, null=True)
	status = models.IntegerField(default=1,null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	reg_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
