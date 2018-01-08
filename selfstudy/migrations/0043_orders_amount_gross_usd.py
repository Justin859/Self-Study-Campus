# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 08:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfstudy', '0042_auto_20180106_0916'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='amount_gross_usd',
            field=models.DecimalField(decimal_places=2, default=12.0, max_digits=9),
            preserve_default=False,
        ),
    ]