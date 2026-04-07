from rest_framework import serializers

from .models import Pet


class PetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    owner_id = serializers.ReadOnlyField(source="owner.id")
    photo = serializers.ImageField(required=False, allow_null=True)

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
            "weight_kg",
            "photo",
            "vaccination_status",
            "medical_notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "owner_id", "created_at", "updated_at")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if instance.photo:
            url = instance.photo.url
            data["photo"] = request.build_absolute_uri(url) if request else url
        else:
            data["photo"] = None
        return data
