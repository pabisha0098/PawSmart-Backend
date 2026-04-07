from django.conf import settings
from django.db import models


class Pet(models.Model):
    class Species(models.TextChoices):
        DOG = "dog", "Dog"
        CAT = "cat", "Cat"
        BIRD = "bird", "Bird"
        OTHER = "other", "Other"

    class VaccinationStatus(models.TextChoices):
        YES = "yes", "Yes"
        NO = "no", "No"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pets")
    name = models.CharField(max_length=120)
    species = models.CharField(max_length=20, choices=Species.choices, default=Species.OTHER)
    breed = models.CharField(max_length=120, blank=True)
    age = models.PositiveIntegerField(default=0)
    weight_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kilograms",
    )
    photo = models.ImageField(upload_to="pets/", blank=True, null=True)
    vaccination_status = models.CharField(
        max_length=10,
        choices=VaccinationStatus.choices,
        default=VaccinationStatus.NO,
    )
    medical_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.species})"
