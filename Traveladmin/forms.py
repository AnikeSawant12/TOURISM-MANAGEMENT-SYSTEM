from django import forms
from travelapp.models import * 
from decimal import Decimal
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.models import User

# Login form view
class LoginForm(AuthenticationForm):
	username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
	password = forms.CharField(
		label=_("Password"),
		strip=False,
		widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}),
	)