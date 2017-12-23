import re

from django import forms

from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# validators

def validate_email(value):
    email = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

    if email.match(value) == None:
        raise ValidationError(
            _('%(value)s is not a valid email address'),
            params={'value': value},
        )

def validate_password(value):
    password = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])(?=.{8,})')

    if password.match(value) == None:
        raise ValidationError(
            _('%(value)s The password does not match the requirements'),
            params={'value': value},
        )

class RegisterForm(forms.Form):
    firstName = forms.CharField(label='First Name', max_length=100, validators=[MinLengthValidator(2, 'Value cant be less than 2 characters')])
    lastName = forms.CharField(label='First Name', max_length=100, validators=[MinLengthValidator(2, 'Value cant be less than 2 characters')])
    emailAddress = forms.EmailField(label='First Name', max_length=100, validators=[validate_email])
    password = forms.CharField(label='Create Password', max_length=255, validators=[validate_password])
    confirmPassword = forms.CharField(label='Confirm Password', max_length=255)

class UserLogin(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(max_length=255)

class AddToCart(forms.Form):
    item_title = forms.CharField(max_length=255)
    item_price = forms.DecimalField(max_digits=6, decimal_places=2)


