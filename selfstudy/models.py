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
        