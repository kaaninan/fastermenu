# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-16 18:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0009_auto_20181016_1553'),
        ('cart', '0007_auto_20181016_2130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waiter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calledDate', models.DateTimeField(editable=False)),
                ('complatedDate', models.DateTimeField(null=True)),
                ('isComplated', models.BooleanField(default=False)),
                ('enterprise', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='enterprise.Enterprise')),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='enterprise.Table')),
            ],
            options={
                'ordering': ['-calledDate'],
            },
        ),
    ]
