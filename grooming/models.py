from django.conf import settings
from django.db import models

from pets.models import Pet


class GroomingService(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class GroomingAppointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="grooming_appointments")
    service = models.ForeignKey(GroomingService, on_delete=models.PROTECT, related_name="appointments")
    groomer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_grooming_appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["appointment_date", "appointment_time"]
