from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UsernameField


# Login form view
class LoginForm(AuthenticationForm):

	email = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control bg-white'}))
	password = forms.CharField(
		label=_("Password"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control bg-white'}),
	)


class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ('cemail', 'cmobileno')


class CustomUserChangeForm(UserChangeForm):
	GENDER_CHOICES = (('Male', 'Male'), ('Female', 'Female'))

	cemail = forms.CharField(
		min_length=2,
		max_length=70,
		widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control bg-white'})
	)

	cfname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter First Name','class': 'form-control bg-white'})
	)
	cmname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Middle Name','class': 'form-control bg-white'})
	)
	clname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name','class': 'form-control bg-white'})
	)

	cgender = forms.ChoiceField(choices = GENDER_CHOICES, label="Select Gender", initial='', widget=forms.Select(attrs={'class': 'form-control bg-white'}), required=True)

	cmobileno = forms.CharField(
		min_length=10,
		max_length=10,
		widget=forms.TextInput(attrs={'placeholder': 'Mobile No','class': 'form-control bg-white'})
	)


	caddress1 = forms.CharField(
		widget=forms.Textarea(attrs={'rows':3, 'cols':5, 'placeholder': 'Enter Address 1','class': 'form-control bg-white'})
	)
	caddress2 = forms.CharField(
		widget=forms.Textarea(attrs={'rows':3, 'cols':5, 'placeholder': 'Enter Address 2','class': 'form-control bg-white'})
	)

	ccity = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter City','class': 'form-control bg-white'})
	)
	cstate = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter State','class': 'form-control bg-white'})
	)

	ccountry = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Country','class': 'form-control bg-white'})
	)

	cpin = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Pin','class': 'form-control bg-white'})
	)

	password = forms.CharField(
		min_length=8,
		max_length=70,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control bg-white'})
	)
	password_confirmation = forms.CharField(
		min_length=8,
		max_length=70,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation','class': 'form-control bg-white'})
	)


	class Meta:
		model = CustomUser
		fields = ['cusername','cemail','cfname', 'cmname', 'clname', 'cgender', 'cmobileno', 'caddress1', 'caddress2', 'ccity', 'cstate', 'ccountry', 'cpin']



# User Creation form
class SignupForm(forms.Form):
	
	GENDER_CHOICES = (('Select Gender', 'Select Gender'),('Male', 'Male'), ('Female', 'Female'))

	cusername = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder': 'Enter username','class': 'form-control bg-white', 'required':'required'})
	)

	cemail = forms.CharField(
		min_length=2,
		max_length=70,
		widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-control bg-white'})
	)

	cfname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter First Name','class': 'form-control bg-white'})
	)
	cmname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Middle Name','class': 'form-control bg-white'})
	)
	clname = forms.CharField(
		min_length=2,
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Last Name','class': 'form-control bg-white'})
	)

	cgender = forms.ChoiceField(choices = GENDER_CHOICES, label="Select Gender", initial='', widget=forms.Select(attrs={'class': 'form-control bg-white'}), required=True)

	cmobileno = forms.CharField(
		min_length=10,
		max_length=10,
		widget=forms.TextInput(attrs={'placeholder': 'Mobile No','class': 'form-control bg-white'})
	)


	caddress1 = forms.CharField(
		widget=forms.Textarea(attrs={'rows':3, 'cols':5, 'placeholder': 'Enter Address 1','class': 'form-control bg-white'})
	)
	caddress2 = forms.CharField(
		widget=forms.Textarea(attrs={'rows':3, 'cols':5, 'placeholder': 'Enter Address 2','class': 'form-control bg-white'})
	)

	ccity = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter City','class': 'form-control bg-white'})
	)
	cstate = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter State','class': 'form-control bg-white'})
	)

	ccountry = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Country','class': 'form-control bg-white'})
	)

	cpin = forms.CharField(
		max_length=300,
		widget=forms.TextInput(attrs={'placeholder': 'Enter Pin','class': 'form-control bg-white'})
	)

	password = forms.CharField(
		min_length=8,
		max_length=70,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control bg-white'})
	)
	password_confirmation = forms.CharField(
		min_length=8,
		max_length=70,
		widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation','class': 'form-control bg-white'})
	)



	class Meta:
		model = CustomUser
		fields = ['cusername','cemail','cfname', 'cmname', 'clname', 'cgender', 'cmobileno', 'caddress1', 'caddress2', 'ccity', 'cstate', 'ccountry', 'cpin']
		
	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)
		self.fields['cusername'].label = "Enter Username"	
		self.fields['password'].required = True
		self.fields['cemail'].label = "Enter Email"
		self.fields['cfname'].label = "Enter First Name"	
		self.fields['cmname'].label = "Enter Middle Name"
		self.fields['clname'].label = "Enter Last"	
		self.fields['cgender'].label = "Select Gender"
		self.fields['cmobileno'].label = "Enter Mobile No"	
		self.fields['caddress1'].label = "Address 1"
		self.fields['caddress2'].label = "Address 1"	
		self.fields['ccity'].label = "Enter City"
		self.fields['cstate'].label = "Enter State"	
		self.fields['ccountry'].label = "Enter Country"
		self.fields['cpin'].label = "Enter Pin"	
	
		
	def clean(self):
		"""Verify password confirmation match."""
		data = super().clean()

		password = data['password']
		password_confirmation = data['password_confirmation']

		if password != password_confirmation:
			raise forms.ValidationError('Passwords do not match.')
		return data

	
	def save(self):
		"""Create user and profile"""
		data = self.cleaned_data
		data.pop('password_confirmation')

		user = CustomUser.objects.create_user(**data)  


# Hotel form class
class HotelForm(forms.ModelForm):
	shotelname = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Hotel Name'}))   

	#hotelimg = forms.ImageField(widget=forms.TextInput
	#(attrs={'class':'form-control', 'type':'file'}))	

	shoteltype =  forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Hotel type'}))	

	sdesc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))			        

	sstatus = forms.IntegerField(widget=forms.HiddenInput(),initial=1)   

	class Meta:
		model = Services
		fields = ['shotelname', 'shotelimg','shoteltype', 'sdesc' , 'sstatus']	

	def __init__(self, *args, **kwargs):
		super(HotelForm, self).__init__(*args, **kwargs)
		self.fields['shotelname'].label = "Enter Hotel Name"	
		self.fields['shoteltype'].label = "Enter Hotel Type"
		self.fields['sdesc'].label = "Enter Description"	
		


class TripsFrom(forms.ModelForm):

	plocation = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Location Name'}))  

	pdays =  forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Days type'}))

	pnights =  forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Nights type'}))	

	pprice =  forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control','placeholder':'Enter Package'}))	

	pfrom_date =  forms.DateField(widget=forms.TextInput
		(attrs={'class':'form-control','type':'date'}))

	pto_date =  forms.DateField(widget=forms.TextInput
		(attrs={'class':'form-control', 'type':'date'}))				

	pday1 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday1_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pday2 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday2_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pday3 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday3_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pday4 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday4_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pday5 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday5_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pday6 = forms.CharField(widget=forms.TextInput
		(attrs={'class':'form-control'}))

	pday6_desc = forms.CharField(widget=forms.Textarea
		(attrs={'class':'form-control', 'rows': 3, 'cols': 5}))

	pstatus = forms.IntegerField(widget=forms.HiddenInput(),initial=1)   

	class Meta:
		model = Package
		fields = ['plocation', 'pdays', 'pnights', 'pprice', 'plocationimg', 'photel', 'pfrom_date', 'pto_date', 'pday1', 'pday1_desc', 'pday2', 'pday2_desc', 'pday3', 'pday3_desc', 'pday4', 'pday4_desc', 'pday5', 'pday5_desc', 'pday6', 'pday6_desc', 'pstatus']	

	def __init__(self, *args, **kwargs):
		super(TripsFrom, self).__init__(*args, **kwargs)
		self.fields['plocation'].label = "Enter Location"	
		self.fields['pdays'].label = "Enter Days"
		self.fields['pnights'].label = "Enter Nights"	
		self.fields['pprice'].label = "Enter Price"
		self.fields['plocationimg'].label = "Select Image"	
		self.fields['photel'].label = "Select Hotel"
		self.fields['pfrom_date'].label = "Enter From Date"	
		self.fields['pto_date'].label = "Enter To Date"
		self.fields['pday1'].label = "Day 1"	
		self.fields['pday1_desc'].label = "Enter Desc"
		self.fields['pday2'].label = "Day 2"	
		self.fields['pday2_desc'].label = "Enter Desc"
		self.fields['pday3'].label = "Day 3"	
		self.fields['pday3_desc'].label = "Enter Desc"
		self.fields['pday4'].label = "Day 4"	
		self.fields['pday4_desc'].label = "Enter Desc"
		self.fields['pday5'].label = "Day 5"	
		self.fields['pday5_desc'].label = "Enter Desc"
		self.fields['pday6'].label = "Day 6"	
		self.fields['pday6_desc'].label = "Enter Desc"
		
		