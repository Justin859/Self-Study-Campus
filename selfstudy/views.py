from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms

from decimal import *

from .forms import *
from .models import *


# Create your views here.
def index(request):
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
    else:
        user_cart = False

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

    return render(request, 'index.html', {'form': form, 'user_cart': user_cart})

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

def course_library(request, course_id, course_title):

    selected_course = Courses.objects.get(id=course_id, title=course_title)

    categories = CourseCategories.objects.all()
    courses = Courses.objects.all().order_by('id')
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
    else:
        user_cart = False

    if request.method == 'POST':
        form = AddToCart(request.POST)
        if form.is_valid():
            title = form.cleaned_data['item_title']
            price = form.cleaned_data['item_price']

        if not user_has_cart:
            cart = UserCart.objects.create(user_id=request.user.id)
            item = CartItems.objects.create(user_id=request.user.id, item_id=selected_course.id, cart_id=cart.id, title=selected_course.title, price=selected_course.price)
            item.save()
            cart.cart_total += float(selected_course.price)
            cart.items_total += 1
            cart.save()
        else:
            cart = UserCart.objects.get(user_id=request.user.id)
            item = CartItems.objects.create(user_id=request.user.id, item_id=selected_course.id, cart_id=cart.id, title=selected_course.title, price=selected_course.price)
            item.save()
            cart.cart_total += round(Decimal(selected_course.price), 2)
            cart.items_total += 1
            cart.save()

        messages.success(request, selected_course.title)
        return HttpResponseRedirect("")
    else:
        form = AddToCart()

    return render(request, 'course_library.html',
     {
     'categories': categories,
     'courses': courses, 'selected_course': selected_course,
     'form': form,
     'user_has_cart': user_has_cart,
     'user_cart': user_cart,
     })

def register(request):
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
        
    return render(request, 'register.html', {'form': form})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

