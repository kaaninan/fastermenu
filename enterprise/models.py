# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _
from barcode.models import *

class Enterprise(models.Model):
    CURRENCY = (
        ('$', _("USD - US Dollar")),
        ('₺', _("TRY - Turkish Lira")),
        ('€', _("EUR - Euro")),
        ('£', _("GBP - Pound")),
    )

    name = models.CharField(max_length=120, verbose_name="Name")
    address = models.CharField(max_length=200, verbose_name="Address", null=True, blank=True)
    phone = models.CharField(max_length=200, verbose_name="Phone", null=True, blank=True)
    size = models.IntegerField(null=True, blank=True, verbose_name="Size")
    logo = models.ImageField(null=True, blank=True, upload_to='logos/')
    active = models.BooleanField(verbose_name="Active", default=True)
    currency = models.CharField(max_length=50, verbose_name="Currency", choices=CURRENCY, default='$')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Table(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    barcode = models.OneToOneField(Barcode, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=120, verbose_name="Name")
    active = models.BooleanField(verbose_name="Active", null=False, default=True)
    # Home Delivery
    client_name = models.CharField(max_length=120, verbose_name="Client Name", null=True, blank=True)
    client_phone = models.CharField(max_length=120, verbose_name="Client Phone", null=True, blank=True)
    client_address = models.CharField(max_length=400, verbose_name="Client Address", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']



class Log(models.Model):
    barcode = models.ForeignKey(Barcode, on_delete=models.SET_NULL, null=True, blank=True)
    barcode_valid = models.BooleanField(default=False)
    barcode_active = models.BooleanField(default=False)
    table_valid = models.BooleanField(default=False)
    table_active = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True, blank=True)
    scanned = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.scanned = datetime.now()
        return super(Log, self).save(*args, **kwargs)

    def __str__(self):
        return self.barcode.barcode

    class Meta:
        ordering = ['-scanned']



from cart.models import Line


class BiotLog(models.Model):
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True, blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True, blank=True)
    scanned = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.scanned = datetime.now()
        return super(BiotLog, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.scanned)

    class Meta:
        ordering = ['-scanned']


class HPLog(models.Model):
    comment = models.CharField(max_length=120, verbose_name="Comment")
    scanned = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        self.scanned = datetime.now()
        return super(HPLog, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.scanned)

    class Meta:
        ordering = ['-scanned']