# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *


class MenuAdmin(admin.ModelAdmin):
    list_display = ['enterprise', 'name', 'price', 'stock']
    list_display_links = ['name']
    search_fields = ['name']

    class Meta:
        model = Menu


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise']
    list_display_links = ['name']
    search_fields = ['name']

    class Meta:
        model = Category


class SubMenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'enterprise']
    list_display_links = ['name']
    search_fields = ['name']

    class Meta:
        model = SubMenuCategory


class SubMenuCategoryOptionAdmin(admin.ModelAdmin):
    list_display = ['menu', 'subMenu', 'name', 'price']
    list_display_links = ['name']
    search_fields = ['name']

    class Meta:
        model = SubMenuCategoryOption


admin.site.register(Menu, MenuAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubMenuCategory, SubMenuCategoryAdmin)
admin.site.register(SubMenuCategoryOption, SubMenuCategoryOptionAdmin)
