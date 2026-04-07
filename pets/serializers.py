from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    owner_id = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Pet
        fields = (
            "id",
            "owner",
            "owner_id",
            "name",
            "species",
            "breed",
            "age",
            "weight",
            "vaccination_status",
            "medical_notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "owner_id", "created_at", "updated_at")
