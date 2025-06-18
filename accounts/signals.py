from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
import logging

@receiver(post_save, sender=User)
def handle_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update a Profile when a User is saved.
    """
    if created:
        Profile.objects.create(user=instance)
        print('Profile created!')
    else:
        instance.profile.save()
        print('Profile updated!')

# signals.py


logger = logging.getLogger('custom')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f"{user.username} başarıyla giriş yaptı. IP: {get_client_ip(request)}")

def get_client_ip(request):
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    return x_forwarded.split(',')[0] if x_forwarded else request.META.get('REMOTE_ADDR')