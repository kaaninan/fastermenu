# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models

class Barcode(models.Model):
    barcode = models.CharField(max_length=120, verbose_name="Barcode")
    active = models.BooleanField(verbose_name="Active", null=False, default=True)

    def __str__(self):
        return self.barcode

    class Meta:
        ordering = ['barcode']