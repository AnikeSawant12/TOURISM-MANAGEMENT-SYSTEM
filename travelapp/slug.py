import string, random
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

# This slug generator for customuser
def unique_slug_generator_user_name(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.cusername)
	Klass = instance.__class__
	max_length = Klass._meta.get_field('slug').max_length
	slug = slug[:max_length]
	qs_exists = Klass.objects.filter(slug = slug).exists()
	
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
			
		return unique_slug_generator_user_name(instance, new_slug = new_slug)
	return slug
  

# This slug generator for Hotel
def unique_slug_generator_hotel(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.shotelname)
	Klass = instance.__class__
	max_length = Klass._meta.get_field('slug').max_length
	slug = slug[:max_length]
	qs_exists = Klass.objects.filter(slug = slug).exists()
	
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
			
		return unique_slug_generator_hotel(instance, new_slug = new_slug)
	return slug



# This slug generator for Trips
def unique_slug_generator_trips(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.plocation)
	Klass = instance.__class__
	max_length = Klass._meta.get_field('slug').max_length
	slug = slug[:max_length]
	qs_exists = Klass.objects.filter(slug = slug).exists()
	
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
			
		return unique_slug_generator_trips(instance, new_slug = new_slug)
	return slug	



# This slug generator for trip reservation
def unique_slug_generator_trips_reservation(instance, new_slug = None):
	if new_slug is not None:
		slug = new_slug
	else:
		slug = slugify(instance.bcname)
	Klass = instance.__class__
	max_length = Klass._meta.get_field('slug').max_length
	slug = slug[:max_length]
	qs_exists = Klass.objects.filter(slug = slug).exists()
	
	if qs_exists:
		new_slug = "{slug}-{randstr}".format(
			slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
			
		return unique_slug_generator_trips_reservation(instance, new_slug = new_slug)
	return slug	

