# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-25 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfstudy', '0023_testsig'),
    ]

    operations = [
        migrations.AddField(
            model_name='testsig',
            name='from_where',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
