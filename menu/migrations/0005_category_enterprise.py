# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-04 23:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0009_auto_20180605_0151'),
        ('menu', '0004_auto_20180605_0215'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='enterprise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='enterprise.Enterprise'),
        ),
    ]
