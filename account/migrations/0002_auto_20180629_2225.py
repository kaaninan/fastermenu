# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-29 19:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='enterprise',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
