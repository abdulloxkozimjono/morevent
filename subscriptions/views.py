from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from datetime import timedelta

from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer):
        # Default expiry: 30 days
        subscription = serializer.save(
            expires_at=now() + timedelta(days=30),
            is_active=True
        )
        return subscription

    @action(detail=True, methods=["post"])
    def renew(self, request, pk=None):
        """Renew subscription by extending 30 days"""
        subscription = self.get_object()
        subscription.expires_at = subscription.expires_at + timedelta(days=30)
        subscription.is_active = True
        subscription.save()
        return Response({"detail": "Subscription renewed successfully."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """Cancel user subscription"""
        subscription = self.get_object()
        subscription.is_active = False
        subscription.save()
        return Response({"detail": "Subscription cancelled."}, status=status.HTTP_200_OK)
