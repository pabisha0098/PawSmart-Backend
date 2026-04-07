from django.contrib.auth import get_user_model
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from appointments.models import VeterinaryAppointment
from pets.models import Pet
from users.permissions import IsAdminRole
from .serializers import UserAdminSerializer, UserRegistrationSerializer, UserSerializer

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserAdminSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role in {"staff", "admin"}:
            users_count = User.objects.count()
            pets_count = Pet.objects.count()
            upcoming_count = VeterinaryAppointment.objects.filter(status__in=["pending", "confirmed"]).count()
        else:
            users_count = 1
            pets_count = Pet.objects.filter(owner=request.user).count()
            upcoming_count = VeterinaryAppointment.objects.filter(
                pet__owner=request.user, status__in=["pending", "confirmed"]
            ).count()
        return Response(
            {
                "total_users": users_count,
                "total_pets": pets_count,
                "upcoming_appointments": upcoming_count,
            }
        )


class StaffListView(APIView):
    """Staff/admin users for vet/groomer assignment dropdowns."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = User.objects.filter(role__in=[User.Roles.STAFF, User.Roles.ADMIN]).order_by(
            "first_name", "last_name", "username"
        )
        data = [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "display_name": (u.get_full_name() or u.username or u.email or "").strip(),
            }
            for u in qs
        ]
        return Response(data)
