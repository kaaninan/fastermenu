# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-30 21:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20180920_0525'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='tip',
            field=models.FloatField(null=True),
        ),
    ]
