# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class BarcodeAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'active']
    list_display_links = ['barcode']

    class Meta:
        model = Barcode



admin.site.register(Barcode, BarcodeAdmin)
