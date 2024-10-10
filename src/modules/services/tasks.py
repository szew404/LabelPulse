from celery import shared_task

from modules.campaigns.models import Campaign
from .senders import send_email

import logging

import datetime

logger = logging.getLogger(__name__)


@shared_task
def send_campaign_emails():
    campaigns = Campaign.objects.filter(
        campaign_sent=False, approved=True, sent_date=datetime.datetime.now()
    )

    for campaign in campaigns:
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
