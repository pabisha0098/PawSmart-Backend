from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ChatbotViewSet

router = DefaultRouter()
router.register("", ChatbotViewSet, basename="chatbot")

urlpatterns = [path("", include(router.urls))]
