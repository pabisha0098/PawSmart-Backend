from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from .models import ServiceHistory, VeterinaryAppointment

User = get_user_model()


class VeterinaryAppointmentSerializer(serializers.ModelSerializer):
    pet_name = serializers.ReadOnlyField(source="pet.name")

    class Meta:
        model = VeterinaryAppointment
        fields = (
            "id",
            "pet",
            "pet_name",
            "assigned_vet",
            "appointment_date",
            "appointment_time",
            "reason",
            "status",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_assigned_vet(self, value):
        if value and value.role not in {"staff", "admin"}:
            raise serializers.ValidationError("Assigned vet must be staff/admin.")
        return value

    def validate(self, attrs):
        assigned_vet = attrs.get("assigned_vet") or getattr(self.instance, "assigned_vet", None)
        date = attrs.get("appointment_date") or getattr(self.instance, "appointment_date", None)
        time = attrs.get("appointment_time") or getattr(self.instance, "appointment_time", None)
        status = attrs.get("status") or getattr(self.instance, "status", None)

        if assigned_vet and date and time and status != "cancelled":
            qs = VeterinaryAppointment.objects.filter(
                assigned_vet=assigned_vet,
                appointment_date=date,
                appointment_time=time,
            ).exclude(status="cancelled")
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError("This vet is already booked for the selected date/time.")
        return attrs


class ServiceHistorySerializer(serializers.ModelSerializer):
    pet_name = serializers.ReadOnlyField(source="pet.name")

    class Meta:
        model = ServiceHistory
        fields = ("id", "pet", "pet_name", "source_type", "source_id", "summary", "completed_at")
