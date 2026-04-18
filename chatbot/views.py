import os
from groq import Groq
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatQuerySerializer

SYSTEM_PROMPT = """You are Paws, a friendly AI assistant for PawSmart Shop — a pet care management platform. You help users with:

1. BOOKING APPOINTMENTS: Vet (Mon–Sat 8am–6pm) and grooming (Mon–Sun 9am–7pm). Collect pet name, service type, and preferred date/time.

2. SERVICES & PRICING:
   - Vet Consultation: $30 (general), $50 (specialist)
   - Vaccinations: $20–$45
   - Grooming – Bath & Dry: $25 (small), $35 (medium), $45 (large)
   - Grooming – Full Groom: $45 (small), $60 (medium), $80 (large)
   - Dental Cleaning: $60
   - Microchipping: $25

3. PET HEALTH ADVICE: Give general advice on nutrition, exercise, common symptoms. Always recommend seeing a vet for serious concerns.

4. PET PROFILES & HISTORY: Help users understand their pet's service history. Ask for pet name if needed.

Keep responses concise, warm, and helpful. Use simple language. Add a paw emoji 🐾 occasionally."""


def call_groq(query: str, history: list[dict] | None = None) -> str:
    client = Groq()  # reads GROQ_API_KEY from env automatically

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history or []
    messages.append({"role": "user", "content": query})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content


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

        # Rebuild conversation history for multi-turn context (last 10 messages)
        past = (
            ChatMessage.objects
            .filter(user=request.user)
            .order_by("-created_at")[:10]
        )
        history = []
        for msg in reversed(past):
            history.append({"role": "user", "content": msg.query})
            history.append({"role": "assistant", "content": msg.response})

        response_text = call_groq(query, history)
        message = ChatMessage.objects.create(
            user=request.user,
            query=query,
            response=response_text,
        )
        return Response(ChatMessageSerializer(message).data, status=status.HTTP_201_CREATED)