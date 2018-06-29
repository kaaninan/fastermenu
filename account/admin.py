from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from account.models import *

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(DjangoUserAdmin):
    list_display = ('enterprise_name', 'username', 'email' ,'is_active','date_joined', 'is_staff')
    list_display_links = ['enterprise_name', 'username', 'email']
    inlines = [ProfileInline]

    def enterprise_name(self, obj):
        try:
            return obj.profile.enterprise.name
        except Exception as e:
            return 'None'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
