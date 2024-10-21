from celery import shared_task

from modules.campaigns.models import Campaign
from .senders import send_email

import logging

import datetime

logger = logging.getLogger(__name__)


def get_campaigns_for_now() -> list[Campaign]:
    """Get the campaigns that are approved and send time is now.

    Returns:
        list[Campaign]: Campaigns objects that matches with the filter
    """
    return Campaign.objects.filter(
        campaign_sent=False, approved=True, sent_date=datetime.datetime.now()
    )


@shared_task
def send_campaign_emails():

    # Get campaigns
    campaigns = get_campaigns_for_now()

    for campaign in campaigns:

        # Split recipients list
        recipient_list = campaign.recipients.split(",") if campaign.recipients else []

        for recipient in recipient_list:
            if recipient:
                try:
                    send_email(instance=campaign, recipient=[recipient])
                    campaign.campaign_sent = True
                    campaign.save()

                    logger.info(f"Email sent to {recipient} for Campaign {campaign.id}")

                except Exception as e:
                    logger.error(
                        f"Error during the task SEND-CAMPAIGN for Campaign {campaign.id}: {e}"
                    )
