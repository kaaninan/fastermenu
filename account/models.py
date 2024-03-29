from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enterprise.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)