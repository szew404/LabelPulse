from django.urls import path, include

from .views import SignUpView, success_signup


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("success/", success_signup, name="signup_success"),
]
