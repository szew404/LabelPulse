from django.urls import path

from .views import SignUpView, success_signup


urlpatterns = [
    path("", SignUpView.as_view(), name="signup"),
    path("success/", success_signup, name="signup-success"),
]
