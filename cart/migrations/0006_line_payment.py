# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-16 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_auto_20181001_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='payment',
            field=models.CharField(default='default', max_length=50),
        ),
    ]
