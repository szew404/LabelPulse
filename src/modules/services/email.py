from django.core.mail import EmailMessage, get_connection
from django.conf import settings


class Email:
    """
    Connect to the SMPT email backend and send emails
    """

    def connect(self):
        return get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        )

    def send_email(self, subject: str, recipient_list: list, message: str) -> int:
        conn = self.connect()  # Get connection

        try:
            msg = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST,
                to=recipient_list,
                connection=conn,
                headers={
                    "Priority": "Urgent",
                    "X-Priority": 1,
                    "Importance": "high",
                },
            )
        except BaseException as e:
            raise print(f"Error while creating email message: {e}")

        # Setup HTML
        msg.content_subtype = "html"

        try:
            return msg.send(
                fail_silently=False,  # Do not return an exception
            )
        except Exception as e:
            raise print(f"Error sending the email: {e}")
