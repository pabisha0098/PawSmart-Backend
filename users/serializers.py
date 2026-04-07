from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "first_name", "last_name", "phone", "role")
        read_only_fields = ("id",)

    def validate_role(self, value):
        request = self.context.get("request")
        if value in {"admin", "staff"} and (not request or not request.user.is_authenticated or request.user.role != "admin"):
            raise serializers.ValidationError("Only admin can create staff/admin accounts.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "staff_type",
            "date_joined",
        )
        read_only_fields = ("id", "role", "staff_type", "date_joined")


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "phone", "role", "staff_type", "is_active")
