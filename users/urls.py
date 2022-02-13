from django.urls import path
from .views import CustomUserCreate, ProfileDetailAPIView

app_name = "users"

urlpatterns = [
    path('register/', CustomUserCreate.as_view(), name="create_user"),
    path('profile/<int:pk>/', ProfileDetailAPIView.as_view(), name="update profile")
]
