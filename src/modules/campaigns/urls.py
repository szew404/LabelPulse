from django.urls import path
from .views import send_test_email_view

urlpatterns = [
    path(
        "send-test-email/<int:campaign_id>/",
        send_test_email_view,
        name="send_test_email",
    ),
]
