from typing import Optional

from .email import Email
from .create_template import render_template_for_email


def send_email(instance: object, recipient: Optional[str] = None):
    subject = f"PROMO RELEASE: {instance.release.artist} - {instance.release.release_title} {instance.release.release_type} - Listen & Download"

    if recipient:
        to = recipient
    else:  # Test case
        to = [instance.test_email_address]

    message = render_template_for_email(instance)

    new_email = Email()
    try:
        new_email.send_email(subject=subject, recipient_list=to, message=message)
    except Exception as e:
        raise print(f"Error calling the send email method: {e}")
