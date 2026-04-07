from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroomingAppointmentViewSet, GroomingServiceViewSet

router = DefaultRouter()
router.register("services", GroomingServiceViewSet, basename="grooming-services")
router.register("appointments", GroomingAppointmentViewSet, basename="grooming-appointments")

urlpatterns = [path("", include(router.urls))]
