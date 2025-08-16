from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    distance_km = serializers.FloatField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id", "title", "description", "category", "type", "date",
            "location_lat", "location_lng", "address", "media", "source",
            "organizer", "is_approved", "created_at", "updated_at", "distance_km"
        )
        read_only_fields = ("organizer", "is_approved", "created_at", "updated_at")
