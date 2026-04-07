from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        PET_OWNER = "pet_owner", "Pet Owner"
        STAFF = "staff", "Staff"
        ADMIN = "admin", "Admin"

    class StaffType(models.TextChoices):
        NONE = "", "Not applicable"
        VET = "vet", "Veterinarian"
        GROOMER = "groomer", "Groomer"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PET_OWNER)
    staff_type = models.CharField(
        max_length=20,
        choices=StaffType.choices,
        blank=True,
        default="",
        help_text="For staff accounts: vet vs grooming portal access.",
    )
    phone = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        self.is_staff = self.role in {self.Roles.STAFF, self.Roles.ADMIN}
        self.is_superuser = self.role == self.Roles.ADMIN
        super().save(*args, **kwargs)
