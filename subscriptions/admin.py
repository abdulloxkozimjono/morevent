from django.contrib import admin
from .models import Subscription, SubscriptionPlan

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'payment_method', 'start_date', 'end_date', 'is_active')
    list_filter = ('plan', 'is_active', 'payment_method')
    search_fields = ('user__username', 'plan__name')

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_days')
    search_fields = ('name',)
