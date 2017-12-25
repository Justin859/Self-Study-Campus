import hashlib
import os
import requests 

from urllib.parse import urlencode
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import formset_factory

from decimal import *

from .forms import *
from .models import *

# Custom methods

def user_is_admin(user):
    users_in_group = Group.objects.get(name='admin').user_set.all()
    
    if user in users_in_group:
        return True
    else:
        return False

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# Create your views here.
def index(request):
    host_ip = get_client_ip(request)

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

    return render(request, 'index.html', {'form': form, 'user_cart': user_cart, 'cart_empty': cart_empty, 'host_ip': host_ip})

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
            messages.success(request, 'Selected items have been removed from your cart.')
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

    rand_value = Currency.objects.get(currency='ZAR').current_rate * user_cart.cart_total

    data = (
        ("merchant_id", "10004715"),
        ("merchant_key", "dhdw9uqzmpzo0"),
        ("return_url", "https://lit-gorge-69771.herokuapp.com/success/"),
        ("cancel_url", "https://lit-gorge-69771.herokuapp.com/cancel/"),
        ("notify_url", "https://lit-gorge-69771.herokuapp.com/notify/"),
        ("name_first", request.user.first_name),
        ("name_last", request.user.last_name),
        ("email_address", request.user.username),
        ("amount", round(rand_value, 2)),
        ("item_name", "Self Study Campus - Order Number : #" + str(user_cart.id)),
        ("item_description", "Self Study Campus Course Order"),
        ("custom_int1", request.user.id),
        ("custom_str1", request.user.username),
        ("payment_method", "cc"),
        ("passphrase", os.environ['PAYFAST_PASSPHRASE'])
    )

    url_data = urlencode(data)

    signature = hashlib.md5(url_data.encode()).hexdigest()

    return render(request, 'checkout.html', {
        'user_cart': user_cart,
        'user_cart_items': user_cart_items,
        'signature': signature,
        'cart_empty': cart_empty,
        'rand_value': round(rand_value, 2)
        })

@csrf_exempt
def notify(request):

    host_ip = get_client_ip(request)
    valid_ip = ['41.74.179.194', '41.74.179.195', '41.74.179.196', '41.74.179.197', '41.74.179.200',
                '41.74.179.201', '41.74.179.203','41.74.179.204', '41.74.179.210', '41.74.179.211',
                '41.74.179.212', '41.74.179.217', '41.74.179.218']

    if host_ip in valid_ip:
        pf_data = request.POST

        user_cart = UserCart.objects.get(user_id=pf_data['custom_int1'])
        user_cart_items = CartItems.objects.filter(user_id=pf_data['custom_int1'])
        user_details = User.objects.get(id=pf_data['custom_int1'])
        
        if pf_data['payment_status'] == 'COMPLETE':
            rand_value = Currency.objects.get(currency='ZAR').current_rate * user_cart.cart_total

            data = (
                ("merchant_id", "10004715"),
                ("merchant_key", "dhdw9uqzmpzo0"),
                ("return_url", "https://lit-gorge-69771.herokuapp.com/success/"),
                ("cancel_url", "https://lit-gorge-69771.herokuapp.com/cancel/"),
                ("notify_url", "https://lit-gorge-69771.herokuapp.com/notify/"),
                ("name_first", user_details.first_name),
                ("name_last", user_details.last_name),
                ("email_address", user_details.username),
                ("amount", round(rand_value, 2)),
                ("item_name", "Self Study Campus - Order Number : #" + str(user_cart.id)),
                ("item_description", "Self Study Campus Course Order"),
                ("custom_int1", user_details.id),
                ("custom_str1", user_details.username),
                ("payment_method", "cc"),
                ("passphrase", os.environ['PAYFAST_PASSPHRASE'])
            )

            url_data = urlencode(data)

            signature = hashlib.md5(url_data.encode()).hexdigest()
            TestSig.objects.create(signature=signature)
            if pf_data['signature'] == signature:
                for item in user_cart_items:
                    UserCourses.objects.create(
                        pf_payment_id= pf_data['pf_payment_id'],
                        user_id=item.user_id,
                        item_id=item.item_id,
                        title=item.title
                        )

                Orders.objects.create(
                pf_payment_id = pf_data['pf_payment_id'],
                payment_status = pf_data['payment_status'],
                item_name = pf_data['item_name'],
                amount_gross = round(Decimal(pf_data['amount_gross']), 2),
                amount_fee = round(Decimal(pf_data['amount_fee']), 2),
                amount_net = round(Decimal(pf_data['amount_net']), 2),
                name_first = pf_data['name_first'],
                name_last = pf_data['name_last'],
                email_address = pf_data['email_address']
                )
                CartItems.objects.filter(user_id=user_details.id).delete()
                UserCart.objects.get(user_id=user_details.id).delete()
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=302)

    return HttpResponse()

@login_required(login_url='/login/')
def cancel(request):

    return render(request, 'cancel.html', {})

@login_required(login_url='/login/')
def success(request):

    return render(request, 'success.html', {})

@login_required(login_url='/login/')
def update_currency(request):
    if not user_is_admin(request.user):

        return HttpResponse(status=403)
    else:
        zar = Currency.objects.get(currency='ZAR') 
        if request.method == 'POST':
            form = UpdateCurrency(request.POST)

            if form.is_valid():
                currency_zar = form.cleaned_data['currency']
                current_rate_usd = form.cleaned_data['current_rate']

                update = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + os.environ['OPENEXCHANGE_APP_ID'] ).json()
                zar.current_rate = round(update['rates']['ZAR'], 2)
                zar.save()
                HttpResponseRedirect('/update-currency/')

                messages.success(request, 'ZAR has been updated')
        else:
            form = UpdateCurrency()

        return render(request, 'update_currency.html', {'form': form, 'zar': zar})
