# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-19 14:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0009_auto_20181016_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=120, verbose_name='Comment')),
                ('scanned', models.DateTimeField(editable=False)),
            ],
            options={
                'ordering': ['-scanned'],
            },
        ),
    ]