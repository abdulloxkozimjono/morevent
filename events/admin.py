from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "date", "is_approved")
    list_filter = ("category", "is_approved")
    search_fields = ("title", "description", "address")
