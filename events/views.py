from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from accounts.permissions import IsBusinessOrAdmin
from core.utils import haversine_km
from datetime import datetime

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all().order_by("-created_at")
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "type", "is_approved"]
    search_fields = ["title", "description", "address", "source"]
    ordering_fields = ["date", "created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsBusinessOrAdmin()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        upcoming = self.request.query_params.get("upcoming")
        if upcoming == "1":
            qs = qs.filter(date__gte=datetime.utcnow())

        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        radius = float(self.request.query_params.get("radius_km", "0") or 0)
        out = []
        if lat and lng and radius > 0:
            lat, lng = float(lat), float(lng)
            for ev in qs:
                d = haversine_km(lat, lng, ev.location_lat, ev.location_lng)
                if d <= radius:
                    ev.distance_km = round(d, 2)
                    out.append(ev)
            out.sort(key=lambda e: getattr(e, "distance_km", 0))
            return out
        return qs

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user, is_approved=(self.request.user.role in ["admin"]))

class EventRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_update(self, serializer):
        obj = self.get_object()
        u = self.request.user
        if u == obj.organizer or u.role in ["admin"] or u.is_staff:
            serializer.save()
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Siz bu eventni tahrirlay olmaysiz.")
