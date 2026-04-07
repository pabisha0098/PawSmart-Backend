from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ServiceHistoryViewSet, VeterinaryAppointmentViewSet

router = DefaultRouter()
router.register("vet", VeterinaryAppointmentViewSet, basename="vet-appointments")
router.register("history", ServiceHistoryViewSet, basename="service-history")

urlpatterns = [path("", include(router.urls))]
