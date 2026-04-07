from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from appointments.models import ServiceHistory
from users.permissions import IsStaffOrAdmin
from .models import GroomingAppointment, GroomingService
from .serializers import GroomingAppointmentSerializer, GroomingServiceSerializer


class GroomingServiceViewSet(viewsets.ModelViewSet):
    serializer_class = GroomingServiceSerializer
    queryset = GroomingService.objects.all()
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [IsAuthenticated(), IsStaffOrAdmin()]
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if user.role in {"staff", "admin"}:
            return GroomingService.objects.all()
        return GroomingService.objects.filter(is_active=True)


class GroomingAppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = GroomingAppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = GroomingAppointment.objects.select_related("pet", "pet__owner", "service", "groomer")
        if user.role in {"staff", "admin"}:
            return queryset
        return queryset.filter(pet__owner=user)

    def perform_update(self, serializer):
        previous = self.get_object()
        instance = serializer.save()
        if previous.status != "completed" and instance.status == "completed":
            instance.completed_at = instance.completed_at or timezone.now()
            instance.save(update_fields=["completed_at"])
            ServiceHistory.objects.get_or_create(
                source_type=ServiceHistory.SourceType.GROOMING,
                source_id=instance.id,
                defaults={
                    "pet": instance.pet,
                    "owner": instance.pet.owner,
                    "summary": f"Grooming completed: {instance.service.name}",
                    "completed_at": instance.completed_at,
                },
            )
