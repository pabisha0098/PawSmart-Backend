from django.conf import settings
from django.db import models

from pets.models import Pet


class VeterinaryAppointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="vet_appointments")
    assigned_vet = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["appointment_date", "appointment_time"]


class ServiceHistory(models.Model):
    class SourceType(models.TextChoices):
        VET = "vet", "Veterinary"
        GROOMING = "grooming", "Grooming"

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="service_history")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_history")
    source_type = models.CharField(max_length=20, choices=SourceType.choices)
    source_id = models.PositiveIntegerField()
    summary = models.TextField()
    completed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]
