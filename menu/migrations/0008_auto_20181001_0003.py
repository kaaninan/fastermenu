# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-30 21:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_auto_20180922_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biot',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.Menu', verbose_name='Please Select Menu'),
        ),
    ]