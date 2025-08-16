from core.models import TimeStampedModel
from django.db import models
from django.conf import settings


class Event(TimeStampedModel):
    CATEGORY_CHOICES = [
        ("concert", "Concert"),
        ("sport", "Sport"),
        ("education", "Education"),
        ("discount", "Discount"),
        ("special", "Special Offer"),
        ("other", "Other"),
    ]
    TYPE_CHOICES = [
        ("once", "One-time"),
        ("recurring", "Recurring"),
        ("discount", "Discount"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="once")

    date = models.DateTimeField()
    location_lat = models.FloatField()
    location_lng = models.FloatField()
    address = models.CharField(max_length=255, blank=True)

    media = models.JSONField(default=list, blank=True)
    source = models.CharField(max_length=100, blank=True)  # Instagram/Telegram link

    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="events")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
