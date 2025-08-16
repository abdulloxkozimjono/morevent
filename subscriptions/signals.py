from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Subscription

@receiver(post_save, sender=Subscription)
def check_subscription_expiry(sender, instance, **kwargs):
    if instance.expires_at and instance.expires_at < now():
        instance.is_active = False
        instance.save()
