from django.urls import path

from .views import SignUpView, success_signup


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signup/success", success_signup, name="signup-success"),
]
