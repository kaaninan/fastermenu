# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-24 17:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0010_hplog'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterprise',
            name='phone',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Phone'),
        ),
    ]
