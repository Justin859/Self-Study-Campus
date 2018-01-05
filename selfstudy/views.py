import hashlib
import os
import requests 
import random

import django_excel as excel
from mohawk import Sender

from dateutil import parser
from dateutil.parser import parse
from datetime import datetime
from urllib.parse import urlencode

from django.db import transaction
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django import forms
from django.forms import formset_factory
from django.core.mail import send_mail

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
    user_admin = user_is_admin(request.user)
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

    return render(request, 'index.html', {'form': form, 'user_cart': user_cart, 'cart_empty': cart_empty, 'user_admin': user_admin})

def user_login(request):
    user_admin = user_is_admin(request.user)
    logout(request)
    next = ""

    if request.GET:  
        next = request.GET['next']

    if request.method == 'POST':

        form = UserLogin(request.POST)

        if form.is_valid():

            user_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=user_email, password=password)
            if user is not None:
                
                login(request, user)
                # Redirect to a success page.
                if next == "":
                    return redirect('/')
                else:
                    return redirect(request.GET['next'])
            elif User.objects.filter(username=user_email).exists():
                messages.error(request, 'Username or Password is incorrect.')
                # Return an 'invalid login' error message.
            else:
                messages.error(request, 'The user does not exist.')
    else:
        form = UserLogin()

    return render(request, 'login_view.html', {'form': form, 'next': next})

def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/')

def course_library(request, course_id, course_title):
    user_admin = user_is_admin(request.user)
    selected_course = Courses.objects.get(id=course_id, title=course_title)

    categories = CourseCategories.objects.all()
    courses = Courses.objects.all().order_by('id')
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()
    item_in_cart = CartItems.objects.filter(user_id=request.user.id, item_id=course_id).exists()
    user_course = UserCourses.objects.filter(user_id=request.user.id, item_id=course_id).exists()

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
        
            messages.success(request, selected_course.title + " has been added to your shopping cart.")
            
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
     'cart_empty': cart_empty,
     'user_course': user_course,
     'user_admin': user_admin
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

@login_required(redirect_field_name='next', login_url='/login/')
def cart_view(request):
    user_admin = user_is_admin(request.user)
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()
    
    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
        CartEditFormSet = formset_factory(CartEdit, extra=user_cart.items_total)
        rand_value = Currency.objects.get(currency='ZAR').current_rate * user_cart.cart_total

    else:
        user_cart = False
        cart_empty = True
        CartEditFormSet = formset_factory(CartEdit)
        rand_value = 0

    if user_cart:
        user_cart_items = CartItems.objects.filter(cart_id=user_cart.id)
    else:
        user_cart_items = False;

    

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
      'cart_empty': cart_empty,
      'rand_value': round(rand_value, 2),
      'user_admin': user_admin
      })

@login_required(redirect_field_name='next', login_url='/login/')
def checkout(request):
    user_admin = user_is_admin(request.user)
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
        rand_value = Currency.objects.get(currency='ZAR').current_rate * user_cart.cart_total
        user_cart_id = user_cart.id
    else:
        user_cart = False
        user_cart_id = 000
        cart_empty = True
        rand_value = 0

    if user_cart:
        user_cart_items = CartItems.objects.filter(cart_id=user_cart.id)
    else:
        user_cart_items = False;

    data = (
        ("merchant_id", "10315552"),
        ("merchant_key", "qi6olaz410k1v"),
        #("merchant_id", "10004715"),
        #("merchant_key", "dhdw9uqzmpzo0"),
        #("return_url", "https://lit-gorge-69771.herokuapp.com/success/"),
        #("cancel_url", "https://lit-gorge-69771.herokuapp.com/cancel/"),
        #("notify_url", "https://lit-gorge-69771.herokuapp.com/notify/"),
        ("return_url", "https://www.selfstudycampus.com/success/"),
        ("cancel_url", "https://www.selfstudycampus.com/cancel/"),
        ("notify_url", "https://www.selfstudycampus.com/notify/"),
        ("name_first", request.user.first_name),
        ("name_last", request.user.last_name),
        ("email_address", request.user.username),
        ("amount", round(rand_value, 2)),
        ("item_name", "Self Study Campus - Order Number : #" + str(user_cart_id)),
        ("item_description", "Self Study Campus Course Order"),
        ("custom_int1", request.user.id),
        ("custom_str1", request.user.username),
        ("payment_method", "cc"),
        ("passphrase", os.environ['PAYFAST_PASSPHRASE'])
    )

    url_data = urlencode(data)
    data_for_payfast = urlencode(data[:14])
    signature = hashlib.md5(url_data.encode()).hexdigest()

    if request.method == 'POST':
        form = PayFastForm(request.POST)
        
        if form.is_valid():
            merchant_id_sent = form.cleaned_data['merchant_id'] 
            merchant_key_sent = form.cleaned_data['merchant_key']
            return_url_sent = form.cleaned_data['return_url']
            cancel_url_sent = form.cleaned_data['cancel_url']
            notify_url_sent = form.cleaned_data['notify_url']
            name_first_sent = form.cleaned_data['name_first']
            name_last_sent = form.cleaned_data['name_last']
            email_addres_sent = form.cleaned_data['email_address']
            amount_sent = form.cleaned_data['amount']
            item_name_sent = form.cleaned_data['item_name']
            item_description_sent = form.cleaned_data['item_description']
            custom_int1_sent = form.cleaned_data['custom_int1']
            custom_str1_sent = form.cleaned_data['custom_str1']
            payment_method_sent = form.cleaned_data['payment_method']
            signature_sent = form.cleaned_data['signature']

            if (merchant_id_sent == data[0][1] and
                merchant_key_sent == data[1][1] and
                return_url_sent == data[2][1] and
                cancel_url_sent == data[3][1] and
                notify_url_sent == data[4][1] and
                name_first_sent == data[5][1] and
                name_last_sent == data[6][1] and
                email_addres_sent == data[7][1] and
                amount_sent == data[8][1] and
                item_name_sent == data[9][1] and
                item_description_sent == data[10][1] and
                custom_int1_sent == data[11][1] and
                custom_str1_sent == data[12][1] and
                payment_method_sent == data[13][1] and
                signature_sent == signature):

                return HttpResponseRedirect('https://www.payfast.co.za/eng/process?' + data_for_payfast)
                #return HttpResponseRedirect('https://sandbox.payfast.co.za/eng/process?' + data_for_payfast)
            else:
                return TemplateResponse(request, 'server_error.html', {})

    else:
        form = PayFastForm()

    return render(request, 'checkout.html', {
        'user_cart': user_cart,
        'user_cart_items': user_cart_items,
        'signature': signature,
        'cart_empty': cart_empty,
        'rand_value': round(rand_value, 2),
        'form': form,
        'user_admin': user_admin
        })

@csrf_exempt
def notify(request):

    host_ip = get_client_ip(request)
    valid_ip = ['41.74.179.194', '41.74.179.195', '41.74.179.196', '41.74.179.197', '41.74.179.200',
                '41.74.179.201', '41.74.179.203','41.74.179.204', '41.74.179.210', '41.74.179.211',
                '41.74.179.212', '41.74.179.217', '41.74.179.218']

    if host_ip in valid_ip:
        pf_data = request.POST

        data = (
            ('m_payment_id', pf_data['m_payment_id']),
            ('pf_payment_id', pf_data['pf_payment_id']),
            ('payment_status', pf_data['payment_status']),
            ('item_name', pf_data['item_name']),
            ('item_description', pf_data['item_description']),
            ('amount_gross', pf_data['amount_gross']),
            ('amount_fee', pf_data['amount_fee']),
            ('amount_net', pf_data['amount_net']),
            ('custom_str1', pf_data['custom_str1']),
            ('custom_str2', pf_data['custom_str2']),
            ('custom_str3', pf_data['custom_str3']),
            ('custom_str4', pf_data['custom_str4']),
            ('custom_str5', pf_data['custom_str5']),
            ('custom_int1', pf_data['custom_int1']),
            ('custom_int2', pf_data['custom_int2']),
            ('custom_int3', pf_data['custom_int3']),
            ('custom_int4', pf_data['custom_int4']),
            ('custom_int5', pf_data['custom_int5']),
            ('name_first', pf_data['name_first']),
            ('name_last', pf_data['name_last']),
            ('email_address', pf_data['email_address']),
            ('merchant_id', pf_data['merchant_id']),
            ('passphrase', os.environ['PAYFAST_PASSPHRASE'])
        )

        url_data = urlencode(data)
        signature = hashlib.md5(url_data.encode()).hexdigest()

        user_cart = UserCart.objects.get(user_id=pf_data['custom_int1'])
        user_cart_items = CartItems.objects.filter(user_id=pf_data['custom_int1'])
        user_details = User.objects.get(id=pf_data['custom_int1'])
        is_paid_user = PaidUser.objects.filter(user_id=user_details.id).exists()

        if signature == pf_data['signature']:
            if pf_data['payment_status'] == 'COMPLETE':
                if not is_paid_user:
                    url = 'https://api.znanja.com/api/hawk/v1/user'
                    method = 'PUT'
                    content_type = 'application/json'
                    content = '{\"first_name\": \"'+user_details.first_name+'\", \"last_name\": \"'+user_details.last_name+'\", \"email\": \"'+pf_data['custom_str1']+'\", \"is_active\": false }'

                    sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                    'key': os.environ['ZNANJA_API_KEY'],
                                    'algorithm': 'sha256'},
                                    url,
                                    method,
                                    content=content,
                                    content_type=content_type)

                    r = requests.put(url, data=content,
                                    headers={'Authorization': sender.request_header,
                                            'Content-Type': content_type})
                    password = ''

                    for i in range(10):
                        password += random.choice(os.environ['PASSWORD_CHARS'])

                    if r.status_code == requests.codes.ok:
                        new_paid_user = PaidUser.objects.create(user_id=pf_data['custom_int1'], portal_id=r.json()['id'], user_name=pf_data['custom_str1'], user_password=password)
                        new_paid_user.save()
                        url = 'https://api.znanja.com/api/hawk/v1/user/' + pf_data['custom_str1']
                        method = 'POST'
                        content_type = 'application/json'
                        content = '{\"first_name\": \"'+user_details.first_name+'\", \"last_name\": \"'+user_details.last_name+'\", \"email\": \"'+pf_data['custom_str1']+'\", \"password\": \"'+password+'\", \"password_confirm\": \"'+password+'\", \"is_active\": false }'

                        sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                        'key': os.environ['ZNANJA_API_KEY'],
                                        'algorithm': 'sha256'},
                                        url,
                                        method,
                                        content=content,
                                        content_type=content_type)

                        rpass = requests.post(url, data=content,
                                        headers={'Authorization': sender.request_header,
                                                'Content-Type': content_type})

                        if rpass.status_code == requests.codes.ok:

                            with transaction.atomic():
                                
                                for item in user_cart_items:
                                    course_voucher = CourseVouchers.objects.filter(course_id=item.item_id, expiry__gt=(datetime.now()))[0]
                                    voucher_total = CourseVouchersTotal.objects.get(course_id=item.item_id)
                                    user_courses = UserCourses.objects.create(
                                        pf_payment_id= pf_data['pf_payment_id'],
                                        user_id=item.user_id,
                                        item_id=item.item_id,
                                        title=item.title,
                                        voucher=course_voucher.code,
                                        voucher_expiry_date=course_voucher.expiry
                                        )
                                    voucher_total.total_vouchers -= 1
                                    course_voucher.delete()
                                    user_courses.save()
                                    voucher_total.save()

                            Orders.objects.create(
                            pf_payment_id = pf_data['pf_payment_id'],
                            user_id = user_details.id,
                            payment_status = pf_data['payment_status'],
                            item_name = pf_data['item_name'],
                            amount_gross = round(Decimal(pf_data['amount_gross']), 2),
                            amount_fee = round(Decimal(pf_data['amount_fee']), 2),
                            amount_net = round(Decimal(pf_data['amount_net']), 2),
                            name_first = user_details.first_name,
                            name_last = user_details.last_name,
                            email_address = pf_data['custom_str1']
                            )
                            CartItems.objects.filter(user_id=user_details.id).delete()
                            UserCart.objects.get(user_id=user_details.id).delete()

                            try:
                                send_mail(
                                        "Self Study Campus User Portal Login Details",
                                        "Welcome to Self Study Campus!\n\n" +
                                        "Please go to https://www.selfstudycampus.com/account/my-courses/\nfor more information and instructions on how to redeem your courses.\n\n" + 
                                        "Portal Login Details:\n\n"
                                        "Email: " + pf_data['custom_str1'] + "\n"
                                        "password: " + password,
                                        'no-reply@selfstudycampus.com',
                                        [pf_data['custom_str1']],
                                        fail_silently=False,
                                        )
                            except BadHeaderError:
                                return HttpResponse('Invalid header found.')
                        else:
                            print(rpass.text)
                            return HttpResponse(status=rpass.status_code)
                    else:
                        print(r.text)
                        return HttpResponse(status=r.status_code)
                else:
                    with transaction.atomic():
                        
                        for item in user_cart_items:
                            course_voucher = CourseVouchers.objects.filter(course_id=item.item_id, expiry__gt=(datetime.now()))[0]
                            voucher_total = CourseVouchersTotal.objects.get(course_id=item.item_id)
                            user_courses = UserCourses.objects.create(
                                pf_payment_id= pf_data['pf_payment_id'],
                                user_id=item.user_id,
                                item_id=item.item_id,
                                title=item.title,
                                voucher=course_voucher.code,
                                voucher_expiry_date=course_voucher.expiry
                                )
                            voucher_total.total_vouchers -= 1
                            course_voucher.delete()
                            user_courses.save()
                            voucher_total.save()

                    Orders.objects.create(
                    pf_payment_id = pf_data['pf_payment_id'],
                    user_id = user_details.id,
                    payment_status = pf_data['payment_status'],
                    item_name = pf_data['item_name'],
                    amount_gross = round(Decimal(pf_data['amount_gross']), 2),
                    amount_fee = round(Decimal(pf_data['amount_fee']), 2),
                    amount_net = round(Decimal(pf_data['amount_net']), 2),
                    name_first = user_details.first_name,
                    name_last = user_details.last_name,
                    email_address = pf_data['custom_str1']
                    )
                    CartItems.objects.filter(user_id=user_details.id).delete()
                    UserCart.objects.get(user_id=user_details.id).delete()
            else:
                return HttpResponse(status=400)
        else:
            return HttpResponse(status=409)
    else:
        return HttpResponse(status=403)
    return HttpResponse()

@login_required(redirect_field_name='next', login_url='/login/')
def cancel(request):

    return HttpResponseRedirect('/shopping-cart/')

@login_required(redirect_field_name='next', login_url='/login/')
def success(request):
    user_admin = user_is_admin(request.user)
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()
    orders = Orders.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1

    else:
        user_cart = False
        cart_empty = True
    
    if orders:
        user_order = Orders.objects.filter(user_id=request.user.id).order_by('-payment_date')[0]
        rand_value = Currency.objects.get(currency='ZAR').current_rate
        usd = user_order.amount_gross / rand_value

        return render(request, 'success.html',
         {'user_cart': user_cart,
          'cart_empty': cart_empty,
          'user_admin': user_admin,
          'usd': usd,
          'user_order': user_order})
    else:
        return HttpResponseBadRequest()

@login_required(redirect_field_name='next', login_url='/login/')
def update_currency(request):
    user_admin = user_is_admin(request.user)
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

        return render(request, 'update_currency.html', {'form': form, 'zar': zar, 'user_admin': user_admin})

@login_required(redirect_field_name='next', login_url='/login/')
def import_data(request):
    user_admin = user_is_admin(request.user)

    if not user_is_admin(request.user):
        return HttpResponse(status=403)
    else:

        vouchers = CourseVouchersTotal.objects.all().order_by('course_id')
        courses = Courses.objects.all().order_by('id')

        if request.method == "POST":
            form = UploadFileForm(request.POST,
                                request.FILES)
            if form.is_valid():
                vouchers = request.FILES['file'].get_array()[1:]
                course_title = form.cleaned_data['course']
                selected_course = Courses.objects.get(title=course_title)
                voucher_total_exists = CourseVouchersTotal.objects.filter(course_id=selected_course.id).exists()
                user_courses = UserCourses.objects.all()
                if not voucher_total_exists:
                    voucher_total = CourseVouchersTotal.objects.create(course=course_title, course_id=selected_course.id)
                else:
                    voucher_total = CourseVouchersTotal.objects.get(course_id=selected_course.id)
                with transaction.atomic():
                    for voucher in vouchers:
                        voucher_already_exits = CourseVouchers.objects.filter(code=voucher[0], course_id=selected_course.id).exists()
                        voucher_with_user = UserCourses.objects.filter(voucher=voucher[0], item_id=selected_course.id).exists()
                        if not voucher_already_exits and not voucher_with_user and voucher[3] == 'No':
                            voucher_added = CourseVouchers.objects.create(course=course_title, course_id=selected_course.id, code=voucher[0], expiry=parser.parse(voucher[1]))
                            voucher_added.save()
                            voucher_total.total_vouchers += 1
                voucher_total.save()
                messages.success(request, "Successfull Upload !")
                return HttpResponseRedirect('/upload-vouchers/')
        else:
            form = UploadFileForm()
        return render(
            request,
            'upload_form.html',
            {
                'form': form,
                'courses': courses,
                'vouchers': vouchers,
                'user_admin': user_admin
            })

@login_required(redirect_field_name='next', login_url='/login/')
def my_courses(request):

    user_admin = user_is_admin(request.user)
    user_courses = UserCourses.objects.filter(user_id=request.user.id).exists()
    has_purchased = PaidUser.objects.filter(user_id=request.user.id).exists()
    orders = Orders.objects.filter(user_id=request.user.id).exists()
    todays_date = datetime.now()

    if orders:
        user_orders = Orders.objects.filter(user_id=request.user.id).order_by('-payment_date')[:4]
        user_more_orders = Orders.objects.filter(user_id=request.user.id).order_by('-payment_date')[4:]
        rand_value = Currency.objects.get(currency='ZAR').current_rate
    else:
        user_orders = False
        user_more_orders = False
        rand_value = 0

    if has_purchased and user_courses:
        user_courses = UserCourses.objects.filter(user_id=request.user.id)
        paid_user = PaidUser.objects.get(user_id=request.user.id)
        course_array = []
        course_category_array = []

        for item in user_courses:
            course_array.append(item.item_id)
    
        courses = Courses.objects.filter(id__in=course_array)

        for category in courses:
            if category.category not in course_category_array:
                course_category_array.append(category.category)

        course_categories = CourseCategories.objects.filter(title__in=course_category_array).order_by('id')

        portal_user_details = (
            ('user_id', str(paid_user.user_id)),
            ('portal_user_id', str(paid_user.portal_id)),
            ('email', paid_user.user_name),
            ('first_name', request.user.first_name),
            ('last_name', request.user.last_name),
            ('passphrase', os.environ['PAYFAST_PASSPHRASE'])
        )

        url_data = urlencode(portal_user_details)
        signature = hashlib.md5(url_data.encode()).hexdigest()

    else:
        user_courses = False
        paid_user = False
        courses = False
        course_categories = False
        portal_user_details = False
        signature = False

    if request.method == 'POST':
        form = PortalPasswordReset(request.POST)

        if form.is_valid():

            user_id = form.cleaned_data['user_id']
            portal_user_id = form.cleaned_data['portal_user_id']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            form_user_details = (
                ('user_id', str(user_id)),
                ('portal_user_id', str(portal_user_id)),
                ('email', email),
                ('first_name', first_name),
                ('last_name', last_name),
                ('passphrase', os.environ['PAYFAST_PASSPHRASE'])
            )

            form_data_url = urlencode(form_user_details)
            signature_from_form = hashlib.md5(form_data_url.encode()).hexdigest()

            if signature_from_form == signature:
                if ProtalPasswordResets.objects.filter(user_id=user_id).exists():
                    current_user = ProtalPasswordResets.objects.get(user_id=user_id)
                    if (datetime.now() - parse(current_user.date_changed.strftime('%m/%d/%Y'))).days > 7:
                        current_user.date_changed = datetime.now()

                        password = ''

                        for i in range(10):
                            password += random.choice(os.environ['PASSWORD_CHARS'])

                        url = 'https://api.znanja.com/api/hawk/v1/user/' + str(portal_user_id)
                        method = 'POST'
                        content_type = 'application/json'
                        content = '{\"first_name\": \"'+first_name+'\", \"last_name\": \"'+last_name+'\", \"email\": \"'+email+'\", \"password\": \"'+password+'\", \"password_confirm\": \"'+password+'\", \"is_active\": false }'

                        sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                        'key': os.environ['ZNANJA_API_KEY'],
                                        'algorithm': 'sha256'},
                                        url,
                                        method,
                                        content=content,
                                        content_type=content_type)

                        rpass = requests.post(url, data=content,
                                        headers={'Authorization': sender.request_header,
                                                'Content-Type': content_type})

                        if rpass.status_code == requests.codes.ok:
                            try:
                                send_mail(
                                        "Self Study Campus User Portal Login Details",
                                        "Welcome to Self Study Campus!\n\n" +
                                        "Please go to https://www.selfstudycampus.com/account/my-courses/\nfor more information and instructions on how to redeem your courses.\n\n" + 
                                        "Portal Login Details:\n\n"
                                        "Email: " + email + "\n"
                                        "password: " + password,
                                        'no-reply@selfstudycampus.com',
                                        [email],
                                        fail_silently=False,
                                        )
                                messages.success(request, "Your password has been reset and a new email has been sent to your Self Study Campus email address")
                            except BadHeaderError:
                                return HttpResponse('Invalid header found.')
                                
                            paid_user.user_password = password
                            paid_user.save()
                        else:
                            messages.error(request, 'An error has ocurred please contact support@selfstudycampus.com for assistance or changeyou password in the portal.')
                            return HttpResponseRedirect('/account/my-courses/')
                    else:
                        messages.error(request, 'Your password has been changed too recently. You can change your password from the portal.')
                        return HttpResponseRedirect('/account/my-courses/')
                else:
                    ProtalPasswordResets.objects.create(user_id=user_id, portal_user_id=portal_user_id)

                    password = ''

                    for i in range(10):
                        password += random.choice(os.environ['PASSWORD_CHARS'])

                    url = 'https://api.znanja.com/api/hawk/v1/user/' + str(portal_user_id)
                    method = 'POST'
                    content_type = 'application/json'
                    content = '{\"first_name\": \"'+first_name+'\", \"last_name\": \"'+last_name+'\", \"email\": \"'+email+'\", \"password\": \"'+password+'\", \"password_confirm\": \"'+password+'\", \"is_active\": false }'

                    sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                    'key': os.environ['ZNANJA_API_KEY'],
                                    'algorithm': 'sha256'},
                                    url,
                                    method,
                                    content=content,
                                    content_type=content_type)

                    rpass = requests.post(url, data=content,
                                    headers={'Authorization': sender.request_header,
                                            'Content-Type': content_type})
                    if rpass.status_code == requests.codes.ok:
                        try:
                            send_mail(
                                    "Self Study Campus User Portal Login Details",
                                    "Welcome to Self Study Campus!\n\n" +
                                    "Please go to https://www.selfstudycampus.com/account/my-courses/\nfor more information and instructions on how to redeem your courses.\n\n" + 
                                    "Portal Login Details:\n\n"
                                    "Email: " + email + "\n"
                                    "password: " + password,
                                    'no-reply@selfstudycampus.com',
                                    [email],
                                    fail_silently=False,
                                    )
                            messages.success(request, "Your password has been reset and a new email has been sent to your Self Study Campus email address")
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        paid_user.user_password = password
                        paid_user.save()
                    else:
                        messages.error(request, 'An error has ocurred please contact support@selfstudycampus.com for assistance or changeyou password in the portal.')
                        return HttpResponseRedirect('/account/my-courses/')
            else:
                messages.error(request, "An Error has occured please contact support@selfstudycampus.com for assistance or change your password in the portal.")
                return HttpResponseRedirect('/account/my-courses/')
    else:
        form = PortalPasswordReset()

    return render(request, 'user_account/my_courses.html',
     {'user_courses': user_courses,
     'paid_user': paid_user,
     'user_admin': user_admin,
     'course_categories': course_categories,
     'courses': courses,
     'rand_value': rand_value,
     'todays_date': todays_date,
     'user_orders': user_orders,
     'user_more_orders': user_more_orders,
     'signature': signature,
     'form': form})

@login_required(redirect_field_name='next', login_url='/login/')
def edit_details(request):

    user_has_orders = Orders.objects.filter(user_id=request.user.id).exists()
    is_paid_user = PaidUser.objects.filter(user_id=request.user.id).exists()

    if request.method == 'POST':

        form = UserEditForm(request.POST)

        if form.is_valid():

            first_name = form.cleaned_data['firstName']
            last_name = form.cleaned_data['lastName']
            email_address = form.cleaned_data['emailAddress']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirmPassword']

            if email_address != request.user.email:

                if User.objects.filter(username=email_address).exists():
                    messages.error(request, '[ '+email_address+' ] ' + 'A user with that email address already exists.')
                else:
                    if is_paid_user:
                        url = 'https://api.znanja.com/api/hawk/v1/user/' +  str(PaidUser.objects.get(user_id=request.user.id).portal_id)
                        method = 'POST'
                        content_type = 'application/json'
                        content = '{\"first_name\": \"'+first_name+'\", \"last_name\": \"'+last_name+'\", \"email\": \"'+email_address+'\", \"is_active\": false }'

                        sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                        'key': os.environ['ZNANJA_API_KEY'],
                                        'algorithm': 'sha256'},
                                        url,
                                        method,
                                        content=content,
                                        content_type=content_type)

                        rpass = requests.post(url, data=content,
                                        headers={'Authorization': sender.request_header,
                                                'Content-Type': content_type})
                        print(rpass)

                        if rpass.status_code != requests.codes.ok:

                            raise forms.ValidationError("user email is already with portal.")
                            print("user email is already with portal.")
                            
                    user = User.objects.get(id=request.user.id)

                    user.username = email_address
                    user.last_name = last_name
                    user.first_name = first_name
                    user.email = email_address

                    if password != confirm_password:
                        raise forms.ValidationError("Passwords do not match")
                    else:

                        if password != "":
                            user.set_password(password)
                        user.save()

                        if user_has_orders:
                            Orders.objects.filter(user_id=request.user.id).update(email_address=email_address)

                        if is_paid_user:
                            PaidUser.objects.filter(user_id=request.user.id).update(user_name=email_address)

                        return HttpResponseRedirect('/login/')
            else:
                if password != confirm_password:
                    raise forms.ValidationError("Passwords do not match")
                else:

                    if is_paid_user:
                        url = 'https://api.znanja.com/api/hawk/v1/user/' +  str(PaidUser.objects.get(user_id=request.user.id).portal_id)
                        method = 'POST'
                        content_type = 'application/json'
                        content = '{\"first_name\": \"'+first_name+'\", \"last_name\": \"'+last_name+'\", \"email\": \"'+email_address+'\", \"is_active\": false }'

                        sender = Sender({'id': os.environ['ZNANJA_API_ID'],
                                        'key': os.environ['ZNANJA_API_KEY'],
                                        'algorithm': 'sha256'},
                                        url,
                                        method,
                                        content=content,
                                        content_type=content_type)

                        rpass = requests.post(url, data=content,
                                        headers={'Authorization': sender.request_header,
                                                'Content-Type': content_type})

                        if rpass.status_code != requests.codes.ok:
                            raise forms.ValidationError("Portal update error.")
                            print("Portal update error.")

                    user = User.objects.get(id=request.user.id)

                    user.last_name = last_name
                    user.first_name = first_name
                    if password != "":
                        user.set_password(password)
                    user.save()

                    return HttpResponseRedirect('/login/')
    else:
        form = UserEditForm()

    return render(request, 'user_account/edit.html', {'form': form})

def contact(request):

    if request.method == 'POST':
        form = Contactform(request.POST)

        if form.is_valid():

            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            emailAddress = form.cleaned_data['emailAddress']
            clientQuery = form.cleaned_data['clientQuery']
            try:
                send_mail(
                        "Self Study Campus Online Query",
                        "Client Name: " + firstName + " " + lastName + "\n\n" +
                        "Query: \n\n" + clientQuery,
                        emailAddress,
                        ['support@selfstudycampus.com'],
                        fail_silently=False,
                        )
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Thank you, " +firstName+ "! Your query has been sent. We will get back to you as soon as possible.")
            return HttpResponseRedirect('/')

    else:
        form = Contactform()

    return render(request, 'contact.html', {'form': form})

def about(request):

    return render(request, 'about.html', {})

@login_required(redirect_field_name='next', login_url='/login/')
def account(request):

    return render(request, 'user_account/account.html', {})

def course_library_main(request):
    user_admin = user_is_admin(request.user)

    categories = CourseCategories.objects.all()
    courses = Courses.objects.all().order_by('id')
    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    return render(request, 'course_library_main.html',
     {
        'categories': categories,
        'courses': courses,
        'user_has_cart': user_has_cart,
        'user_cart': user_cart,
        'cart_empty': cart_empty,
        'user_admin': user_admin
     })

def faq(request):
    user_admin = user_is_admin(request.user)

    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    return render(request, 'faq.html',
     {
        'user_has_cart': user_has_cart,
        'user_cart': user_cart,
        'cart_empty': cart_empty,
        'user_admin': user_admin
     })

def terms(request):
    user_admin = user_is_admin(request.user)

    user_has_cart = UserCart.objects.filter(user_id=request.user.id).exists()

    if user_has_cart:
        user_cart = UserCart.objects.get(user_id=request.user.id)
        cart_empty = user_cart.items_total < 1
    else:
        user_cart = False
        cart_empty = True

    return render(request, 'terms.html',
     {
        'user_has_cart': user_has_cart,
        'user_cart': user_cart,
        'cart_empty': cart_empty,
        'user_admin': user_admin
     })