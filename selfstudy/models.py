from django.db import models
from .models import *

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class CourseCategories(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Course Category'
        verbose_name_plural = 'Course Categories'

list_categories = []
for category in CourseCategories.objects.all():
    list_categories.append((category, category))
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