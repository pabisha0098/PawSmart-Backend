from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import ServiceHistory, VeterinaryAppointment
from .serializers import ServiceHistorySerializer, VeterinaryAppointmentSerializer


class VeterinaryAppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = VeterinaryAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = VeterinaryAppointment.objects.select_related("pet", "pet__owner", "assigned_vet")
        if user.role in {"staff", "admin"}:
            return queryset
        return queryset.filter(pet__owner=user)

    def perform_update(self, serializer):
        previous = self.get_object()
        instance = serializer.save()
        if previous.status != "completed" and instance.status == "completed":
            ServiceHistory.objects.get_or_create(
                source_type=ServiceHistory.SourceType.VET,
                source_id=instance.id,
                defaults={
                    "pet": instance.pet,
                    "owner": instance.pet.owner,
                    "summary": f"Vet appointment completed: {instance.reason}",
                    "completed_at": timezone.now(),
                },
            )


class ServiceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ServiceHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ServiceHistory.objects.select_related("pet", "owner")
        pet_id = self.request.query_params.get("pet")
        if user.role not in {"staff", "admin"}:
            queryset = queryset.filter(owner=user)
        if pet_id:
            queryset = queryset.filter(pet_id=pet_id)
        return queryset
