# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-29 13:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('selfstudy', '0038_orders_order_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_date',
        ),
        migrations.AddField(
            model_name='usercourses',
            name='purchased_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
