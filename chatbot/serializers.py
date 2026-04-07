from rest_framework import serializers

from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ("id", "query", "response", "created_at")
        read_only_fields = ("id", "response", "created_at")


class ChatQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
