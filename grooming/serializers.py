from django.utils import timezone
from rest_framework import serializers

from .models import GroomingAppointment, GroomingService


class GroomingServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroomingService
        fields = "__all__"


class GroomingAppointmentSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source="service.name")
    pet_name = serializers.ReadOnlyField(source="pet.name")

    class Meta:
        model = GroomingAppointment
        fields = (
            "id",
            "pet",
            "pet_name",
            "service",
            "service_name",
            "groomer",
            "appointment_date",
            "appointment_time",
            "status",
            "notes",
            "completed_at",
            "created_at",
        )
        read_only_fields = ("id", "completed_at", "created_at")

    def validate_groomer(self, value):
        if value and value.role not in {"staff", "admin"}:
            raise serializers.ValidationError("Assigned groomer must be staff/admin.")
        return value
