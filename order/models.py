# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from menu.models import *
from enterprise.models import *


class Line(models.Model):
    orderDate = models.DateTimeField(editable=False)
    complatedDate = models.DateTimeField(null=True)
    isComplated = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    totalPrice = models.FloatField(null=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.orderDate = datetime.now()
        return super(Line, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-orderDate']



class Order(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField()
    options = models.CharField(max_length=300, verbose_name="Options")
    optionsReadable = models.CharField(max_length=300, verbose_name="Options Readable", null=True)
    price = models.FloatField()
    totalPrice = models.FloatField()
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.menu.name

    class Meta:
        ordering = ['-menu']


