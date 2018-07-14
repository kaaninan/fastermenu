# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    list_display_links = ['name']
    search_fields = ['name']

    class Meta:
        model = Enterprise

class TableAdmin(admin.ModelAdmin):
    list_display = ['enterprise', 'barcode', 'name']
    list_display_links = ['enterprise', 'barcode', 'name']
    search_fields = ['name']

    class Meta:
        model = Table

class LogAdmin(admin.ModelAdmin):
    list_display = ['barcode', 'scanned', 'barcode_active', 'table_active', 'enterprise']
    list_display_links = ['barcode', 'scanned']

    class Meta:
        model = Log


admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Log, LogAdmin)
