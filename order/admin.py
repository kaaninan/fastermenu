# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['menu', 'enterprise']
    list_display_links = ['enterprise', 'menu']
    search_fields = ['menu']

    class Meta:
        model = Order


class LineAdmin(admin.ModelAdmin):
    list_display = ['enterprise', 'orderDate']
    list_display_links = ['enterprise', 'orderDate']

    class Meta:
        model = Line


admin.site.register(Order, OrderAdmin)
admin.site.register(Line, LineAdmin)
