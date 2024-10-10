from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Campaign
from modules.services.senders import send_email


def send_test_email_view(request, campaign_id):

    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.test_email_address:
        send_email(campaign)
        campaign.test_sent = True
        campaign.save()
        messages.success(
            request, f"Test email sent successfully to {campaign.test_email_address}"
        )
    else:
        messages.error(request, "Error sending the email test.")

    return redirect(request.META.get("HTTP_REFERER", "/"))
