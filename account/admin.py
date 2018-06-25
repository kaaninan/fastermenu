from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from account.models import *

class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name','is_active','date_joined', 'is_staff')
    inlines = [ProfileInline]

    def salary(self, instance):
        try:
            return instance.professor.salary
        except Professor.DoesNotExist:
            return "N/A"

    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        # To reduce database calls
        return qs.select_related('student', 'professor')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
