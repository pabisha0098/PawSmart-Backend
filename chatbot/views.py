from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatQuerySerializer


def mock_llm_response(query: str) -> str:
    return (
        "PawSmart assistant: I received your message - "
        f"'{query}'. This is a mock response. Connect your preferred LLM provider here."
    )


class ChatbotViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatMessage.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="query")
    def query(self, request):
        serializer = ChatQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.validated_data["query"]
        response_text = mock_llm_response(query)
        message = ChatMessage.objects.create(user=request.user, query=query, response=response_text)
        return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)
