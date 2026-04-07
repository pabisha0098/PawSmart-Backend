from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardStatsView, ProfileView, RegistrationView, StaffListView, UserAdminViewSet

router = DefaultRouter()
router.register("admin-users", UserAdminViewSet, basename="admin-users")

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("dashboard-stats/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("staff/", StaffListView.as_view(), name="staff-list"),
    path("", include(router.urls)),
]
