# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-09-02 22:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_category_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='ordering',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='menusubcategory',
            name='ordering',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='menusubcategoryoption',
            name='ordering',
            field=models.IntegerField(null=True),
        ),
    ]