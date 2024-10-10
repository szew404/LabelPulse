from django.core.mail import EmailMessage, get_connection
from django.conf import settings


class Email:

    def connect(self):
        return get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
        )

    def send_email(self, subject: str, recipient_list: list, message: str):
        conn = self.connect()
        try:
            msg = EmailMessage(
                subject=subject,
                body=message,
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
                connection=conn,
            )
        except BaseException as e:
            raise print(f"Error while creating email message: {e}")

        msg.content_subtype = "html"
        try:
            return msg.send()
        except Exception as e:
            raise print(f"Error sending the email: {e}")
