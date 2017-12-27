import re

from django import forms

from django.core.validators import MinLengthValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Courses

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

class CartEdit(forms.Form):
    item_id = forms.IntegerField()
    item_price = forms.DecimalField(max_digits=6, decimal_places=2)
    item_checked = forms.BooleanField(required=False)

class UpdateCurrency(forms.Form):
    currency = forms.CharField(max_length=255)
    current_rate = forms.DecimalField(max_digits=9, decimal_places=2)

class PayFastForm(forms.Form):
    merchant_id = forms.CharField(max_length=255)
    merchant_key = forms.CharField(max_length=255)
    return_url = forms.CharField(max_length=550)
    cancel_url = forms.CharField(max_length=550)
    notify_url = forms.CharField(max_length=255)
    name_first = forms.CharField(max_length=255)
    name_last = forms.CharField(max_length=255)
    email_address = forms.EmailField(max_length=255)
    amount = forms.DecimalField(max_digits=9, decimal_places=2)
    item_name = forms.CharField(max_length=255)
    item_description = forms.CharField(max_length=255)
    custom_int1 = forms.IntegerField()
    custom_str1 = forms.CharField(max_length=255)
    payment_method = forms.CharField(max_length=2)
    signature = forms.CharField(max_length=255)

list_courses = []

for course in Courses.objects.all():
    list_courses.append((course.title, course.title))

COURSES_LIST = tuple(list_courses)

class UploadFileForm(forms.Form):
    course = forms.ChoiceField(choices=COURSES_LIST)
    file = forms.FileField(validators=[FileExtensionValidator(['xls', 'xlsx', 'ods', 'csv'], 'Incorect file extension.')])