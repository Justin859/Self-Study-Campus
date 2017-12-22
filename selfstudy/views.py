from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

from .forms import *
from .models import *


# Create your views here.
def index(request):
    
    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            email_address = form.cleaned_data['emailAddress']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirmPassword']

            if User.objects.filter(username=email_address).exists():
                messages.error(request, '[ '+email_address+' ] ' + 'A user with that email address already exists.')
            else:
                if password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
                else:
                    user = User.objects.create_user(email_address, email_address, password)

                    user.last_name = last_name
                    user.first_name = first_name
                    user.save()

                    return HttpResponseRedirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'index.html', {'form': form})

def user_login(request):

    if request.method == 'POST':

        form = UserLogin(request.POST)

        if form.is_valid():

            user_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=user_email, password=password)
            if user is not None:
                
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            elif User.objects.filter(username=user_email).exists():
                messages.error(request, 'Username or Password is incorrect.')
                # Return an 'invalid login' error message.
            else:
                messages.error(request, 'The user does not exist.')
    else:
        form = UserLogin()

    return render(request, 'login_view.html', {'form': form})

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')

def course_library(request, course_id):

    selected_course = Courses.objects.get(id=course_id)

    categories = CourseCategories.objects.all()
    courses = Courses.objects.all().order_by('id')

    return render(request, 'course_library.html', {'categories': categories, 'courses': courses, 'selected_course': selected_course})

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

