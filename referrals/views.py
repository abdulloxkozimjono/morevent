from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Referral
from .serializers import ReferralSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        referral_code = request.data.get("referral_code")
        invited_by = None

        if referral_code:
            try:
                invited_by = Referral.objects.get(code=referral_code).invited_user
            except Referral.DoesNotExist:
                return Response(
                    {"error": "Invalid referral code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        referral = Referral.objects.create(
            invited_by=invited_by,
            invited_user=request.user,
        )
        serializer = self.get_serializer(referral)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
