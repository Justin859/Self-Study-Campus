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

class CourseImages(models.Model):

    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    course_image = models.ImageField(upload_to='images/course_images/book', max_length=255, null=True, blank=True)    
    course_image_main = models.ImageField(upload_to='images/course_images/main', max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=180.00)

    def __str__(self):
        return self.title + " " + str(self.price)
    
    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Course'

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
    title = models.CharField(max_length=255)
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
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + " " + self.title
        
    class Meta:
        verbose_name = 'User Course'
        verbose_name_plural = 'User Courses'

class Orders(models.Model):
    pf_payment_id = models.IntegerField()
    user_id = models.IntegerField()
    payment_status = models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    amount_gross_usd = models.DecimalField(max_digits=9, decimal_places=2)
    amount_gross = models.DecimalField(max_digits=9, decimal_places=2)
    amount_fee = models.DecimalField(max_digits=9, decimal_places=2)
    amount_net = models.DecimalField(max_digits=9, decimal_places=2)
    name_first = models.CharField(max_length=255)
    name_last = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pf_payment_id) + " | " + self.email_address
        
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class PaidUser(models.Model):
    user_id = models.IntegerField()
    portal_id = models.IntegerField()
    user_name = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name
        
    class Meta:
        verbose_name = 'Paid User'
        verbose_name_plural = 'Paid users'

class CourseVouchers(models.Model):
    course = models.CharField(max_length=500)
    course_id = models.IntegerField()
    code = models.CharField(max_length=255)
    expiry = models.DateTimeField()

    def __str__(self):
        return "Course: " + self.course + " | Expriy Date: " + self.expiry.strftime('%m/%d/%Y') + " | Voucher: " + self.code

    class Meta:
        verbose_name = 'Course Voucher'
        verbose_name_plural = 'Course Vouchers'

class CourseVouchersTotal(models.Model):
    course = models.CharField(max_length=255)
    course_id = models.IntegerField()
    total_vouchers = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course + " " + str(self.total_vouchers)
        
    class Meta:
        verbose_name = 'Voucher Total'
        verbose_name_plural = 'Voucher Totals'

class ProtalPasswordResets(models.Model):
    user_id = models.IntegerField()
    portal_user_id = models.IntegerField()
    date_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + " | " + str(self.portal_user_id) + " | " + self.date_changed.strftime("%m/%d/%Y")

    class Meta:
        verbose_name = 'Portal Password Reset'
        verbose_name_plural = 'Portal Password Resets'
    