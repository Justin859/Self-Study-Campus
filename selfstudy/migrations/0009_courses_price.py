# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfstudy', '0008_auto_20171221_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='price',
            field=models.DecimalField(decimal_places=2, default=180.0, max_digits=6),
        ),
    ]
