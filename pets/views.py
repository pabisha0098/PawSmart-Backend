from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Pet
from .serializers import PetSerializer


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role in {"staff", "admin"}:
            return Pet.objects.all().select_related("owner")
        return Pet.objects.filter(owner=user).select_related("owner")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
