from django.contrib import admin
from .models import Referral

@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("code", "invited_by", "invited_user", "created_at")
    search_fields = ("code", "invited_by__username", "invited_user__username")
