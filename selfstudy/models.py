from django.db import models
from .models import *

# Create your models here.

class CourseCategories(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

list_categories = []
list_courses = []

for category in CourseCategories.objects.all():
    list_categories.append((category.title, category.title))

COURSE_CATEGORIES = tuple(list_categories)

class Courses(models.Model):
    
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=COURSE_CATEGORIES)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=180.00)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

for course in Courses.objects.all():
    list_courses.append((course.title, course.title))

COURSES_LIST = tuple(list_courses)

class UserCart(models.Model):

    user_id = models.IntegerField()
    cart_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    items_total = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_id)
    
    class Meta:
        verbose_name = 'User Cart'
        verbose_name_plural = 'user Carts'

class CartItems(models.Model):

    user_id = models.IntegerField()
    item_id = models.IntegerField()
    cart_id = models.IntegerField()
    title = models.CharField(max_length=255, choices=COURSES_LIST)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return str(self.user_id) + " " + self.title
    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

class Currency(models.Model):

    currency = models.CharField(max_length=255)
    current_rate = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.currency
        
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

class UserCourses(models.Model):

    pf_payment_id = models.IntegerField()
    user_id = models.IntegerField()
    item_id = models.IntegerField()
    title = models.CharField(max_length=255)
    voucher = models.CharField(max_length=255)
    voucher_expiry_date = models.CharField(max_length=255)

    def __str__(self):
        return self.user_id + " " + self.title
        
    class Meta:
        verbose_name = 'User Course'
        verbose_name_plural = 'User Courses'

class Orders(models.Model):
    pf_payment_id = models.IntegerField()
    payment_status = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    amount_gross = models.DecimalField(max_digits=9, decimal_places=2)
    amount_fee = models.DecimalField(max_digits=9, decimal_places=2)
    amount_net = models.DecimalField(max_digits=9, decimal_places=2)
    name_first = models.CharField(max_length=255)
    name_last = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)

class Vouchers(models.Model):
    course = models.CharField(max_length=500, choices=COURSES_LIST)
    course_id = models.IntegerField()
    code = models.CharField(max_length=255)
    expiry = models.CharField(max_length=255)

    def __str__(self):
        return "Course: " + self.course + " | Expriy Date: " + self.expiry
        
    class Meta:
        verbose_name = 'Course Voucher'
        verbose_name_plural = 'Course Vouchers'

class VouchersTotal(models.Model):
    course = models.CharField(max_length=255, choices=COURSES_LIST)
    course_id = models.IntegerField()
    expiry = models.CharField(max_length=255)
    total_vouchers = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course + " " + str(self.total_vouchers)
        
    class Meta:
        verbose_name = 'Voucher Total'
        verbose_name_plural = 'Voucher Totals'

class PaidUser(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name
        
    class Meta:
        verbose_name = 'Paid User'
        verbose_name_plural = 'Paid users'