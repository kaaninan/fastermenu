# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-16 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0005_enterprise_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='currency',
            field=models.CharField(choices=[('USD', '$ - US Dollar'), ('TRY', '₺ - Turkish Lira'), ('EUR', '€ - Euro'), ('GBP', '£ - Pound')], default='1', max_length=50, verbose_name='Currency'),
        ),
    ]
