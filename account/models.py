from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from enterprise.models import *

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = UserProfile(user=user)
        profile.save()