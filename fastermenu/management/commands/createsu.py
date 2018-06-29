from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from account.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            uesr = User.objects.create_superuser("admin", "admin@admin.com", "admin")
            Profile.objects.create(user=user)