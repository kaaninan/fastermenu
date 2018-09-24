# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from enterprise.models import *

class Category(models.Model):
    name = models.CharField(max_length=120, verbose_name="Name")
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)
    ordering = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering']



class Menu(models.Model):
    name = models.CharField(max_length=120, verbose_name="Name")
    picture = models.ImageField(null=True, blank=True, upload_to='menus/')
    description = models.CharField(null=True, blank=True, max_length=120, verbose_name="Description")
    price = models.FloatField(null=False)
    stock = models.BooleanField(verbose_name="Stock", default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)
    ordering = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']



class MenuSubCategory(models.Model):
    TYPES = (
        ('option', 'Option'),
        ('dropadd', 'Drop-Add'),
    )
    name = models.CharField(max_length=120, verbose_name="Name")
    type = models.CharField(verbose_name="Type", choices=TYPES, max_length=100, default='option')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)
    ordering = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']




class MenuSubCategoryOption(models.Model):
    subMenu = models.ForeignKey(MenuSubCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, verbose_name="Name")
    price = models.FloatField(null=False)
    ordering = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    # @property
    # def sorted_attendee_set(self):
    #     return self.attendee_set.order_by('name')

    class Meta:
        ordering = ['price']



class Biot(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, verbose_name=_('Please Select Menu'))
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.pk)





