import hashlib
from urllib.parse import urlencode
import os

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from django.forms import formset_factory

from decimal import *

from .forms import *
from .models import *

# Create your views here.
def index(request):
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

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

    return render(request, 'index.html', {'form': form, 'user_cart': user_cart, 'cart_empty': cart_empty})

def user_login(request):
    logout(request)
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
    item_in_cart = CartItems.objects.filter(user_id=request.user.id, item_id=course_id).exists()
    
    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    if request.method == 'POST':
        form = AddToCart(request.POST)
        if form.is_valid():
            title = form.cleaned_data['item_title']
            price = form.cleaned_data['item_price']
        if not item_in_cart:
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
            
        return HttpResponseRedirect("/course-library/" +course_id+ "/" +course_title+ "/detail")
    else:
        form = AddToCart()

    return render(request, 'course_library.html',
     {
     'categories': categories,
     'courses': courses, 'selected_course': selected_course,
     'form': form,
     'user_has_cart': user_has_cart,
     'user_cart': user_cart,
     'item_in_cart': item_in_cart,
     'cart_empty': cart_empty
     })

def register(request):
    logout(request)
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

@login_required(login_url='/login/')
def cart_view(request):
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()
    
    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    if user_cart:
        user_cart_items = CartItems.objects.filter(cart_id=user_cart.id)
    else:
        user_cart_items = False;

    CartEditFormSet = formset_factory(CartEdit, extra=user_cart.items_total)

    if request.method == 'POST':
        formset = CartEditFormSet(request.POST)
        if formset.is_valid():
            for item in formset.cleaned_data:
                if item['item_checked']:
                    CartItems.objects.filter(id=item['item_id'], user_id=request.user.id).delete()
                    user_cart.items_total -= 1
                    user_cart.cart_total -= item['item_price']
            user_cart.save()
            return HttpResponseRedirect('/shopping-cart/')
    else:
        formset = CartEditFormSet()
    
    return render(request, 'cart_view.html',
     {'user_has_cart': user_has_cart,
      'user_cart': user_cart,
      'user_cart_items': user_cart_items,
      'formset': formset,
      'cart_empty': cart_empty
      })

@login_required(login_url='/login/')
def checkout(request):

    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    if user_cart:
        user_cart_items = CartItems.objects.filter(cart_id=user_cart.id)
    else:
        user_cart_items = False;

    data = (
        ("merchant_id", "10004715"),
        ("merchant_key", "dhdw9uqzmpzo0"),
        ("return_url", "https://lit-gorge-69771.herokuapp.com/success/"),
        ("cancel_url", "https://lit-gorge-69771.herokuapp.com/cancel/"),
        ("notify_url", "https://lit-gorge-69771.herokuapp.com/notify/"),
        ("name_first", request.user.first_name),
        ("name_last", request.user.last_name),
        ("email_address", request.user.username),
        ("amount", user_cart.cart_total),
        ("item_name", "Self Study Campus - Order Number : #" + str(user_cart.id)),
        ("item_description", "Self Study Campus Course Order"),
        ("custom_int1", request.user.id),
        ("custom_str1", request.user.username),
        ("payment_method", "cc"),
        ("passphrase", os.environ['PAYFAST_PASSPHRASE'])
    )

    url_data = urlencode(data)

    signature = hashlib.md5(url_data.encode()).hexdigest()

    return render(request, 'checkout.html', {'user_cart': user_cart, 'user_cart_items': user_cart_items, 'signature': signature, 'cart_empty': cart_empty})

@csrf_exempt
def notify(request):
    
    pf_data = request.POST

    return HttpResponse()

@login_required(login_url='/accounts/login/')
def cancel(request):

    return render(request, 'cancel.html', {})

@login_required(login_url='/accounts/login/')
def success(request):

    return render(request, 'success.html', {})

