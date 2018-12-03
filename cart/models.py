# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.utils.timesince import timesince
from django.db import models

from menu.models import *
from enterprise.models import *


class Line(models.Model):
    orderDate = models.DateTimeField(editable=False)
    complatedDate = models.DateTimeField(null=True)
    canceledDate = models.DateTimeField(null=True)
    paidDate = models.DateTimeField(null=True)
    isCanceled = models.BooleanField(default=False)
    isComplated = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)
    isPrinted = models.BooleanField(default=False)
    isCommented = models.BooleanField(default=False)
    payment = models.CharField(default='default', max_length=50)
    totalPrice = models.FloatField(null=True) # tip + price
    tip = models.FloatField(null=True) # tip $
    price = models.FloatField(null=True) # only price without tip
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True)

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
    line = models.ForeignKey(Line, on_delete=models.CASCADE, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.menu.name

    class Meta:
        ordering = ['-menu']



class Comment(models.Model):
    comment = models.CharField(max_length=300, verbose_name="Comment")
    commentDate = models.DateTimeField(null=True)
    line = models.ForeignKey(Line, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-commentDate']


class Waiter(models.Model):
    calledDate = models.DateTimeField(editable=False)
    complatedDate = models.DateTimeField(null=True)
    isComplated = models.BooleanField(default=False)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['-calledDate']