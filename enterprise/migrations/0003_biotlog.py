# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-10-06 21:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise', '0002_auto_20181001_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiotLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scanned', models.DateTimeField(editable=False)),
                ('enterprise', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='enterprise.Enterprise')),
                ('table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='enterprise.Table')),
            ],
            options={
                'ordering': ['-scanned'],
            },
        ),
    ]
