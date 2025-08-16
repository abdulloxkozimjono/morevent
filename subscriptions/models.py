from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ("basic", "Basic"),
        ("standard", "Standard"),
        ("premium", "Premium"),
    )
    name = models.CharField(max_length=50, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField()  # nechta kun amal qiladi
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.get_name_display()} ({self.price}$)"


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscriptions")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    payment_method = models.CharField(
        max_length=50,
        choices=[("card", "Card"), ("crypto", "Crypto"), ("manual", "Manual")],
        default="manual"
    )

    def save(self, *args, **kwargs):
        # Yangi obuna bo'lsa tugash sanasini avtomatik hisoblaydi
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        # Obuna muddati tugagan bo‘lsa, is_active ni o‘chiradi
        if self.end_date < timezone.now():
            self.is_active = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} → {self.plan.name} ({'Active' if self.is_active else 'Expired'})"
