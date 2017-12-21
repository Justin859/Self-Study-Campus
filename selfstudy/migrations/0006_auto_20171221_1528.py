# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-21 13:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selfstudy', '0005_chatusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tile', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Management', 'Management'), ('Career Development', 'Career Development'), ('Workplace Essentials', 'Workplace Essentials'), ('Sales and Marketing', 'Sales and Marketing'), ('Entrepreneur Training', 'Entrepreneur Training'), ('Human Resources', 'Human Resources'), ('Computer Skills', 'Computer Skills')], max_length=255)),
                ('description', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Courses',
                'verbose_name': 'Course',
            },
        ),
        migrations.DeleteModel(
            name='ChatUsers',
        ),
    ]
