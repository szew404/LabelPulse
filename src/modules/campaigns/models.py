from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_delete, post_save
from django.dispatch import receiver

from modules.services.create_template import create_template
from modules.labels.models import Release, Label
from modules.services.storage_backends import MediaStorage

from src.utils import (
    validate_upload,
    upload_path,
)


class Campaign(models.Model):

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    # Label
    label = models.ForeignKey(
        Label,
        on_delete=models.CASCADE,
        related_name="campaign_label",
    )

    # Release
    release = models.ForeignKey(
        Release,
        on_delete=models.CASCADE,
        null=True,
        related_name="campaign_release",
        blank=False,
    )
    release_banner = models.ImageField(
        upload_to=upload_path,
        storage=MediaStorage(),
        help_text="This banner will be the header of the promotional email. Required size: 1200px width - 400px height",
        default="default-images/banner-default.jpg",
        blank=False,
        null=False,
    )

    # Campaign settings
    sent_date = models.DateTimeField(
        blank=False,
        null=False,
        help_text="Date you want your promotion to be sent. Set a time without minutes, e.g. 04:00:00 as the system updates every 60 minutes.",
    )
    recipients = models.TextField(
        "Recipients' e-mail addresses",
        max_length=2500,
        help_text="Paste a list of email addresses separated by commas. Maximum allowed: 100",
        blank=False,
        null=False,
        default="gidaszewskifranco@gmail.com",
    )
    campaign_sent = models.BooleanField(default=False)

    # Test campaign
    test_email_address = models.EmailField(
        help_text="E-mail address to send a test message."
    )
    test_sent = models.BooleanField(default=False)

    # HTML Template File -Auto created
    template = models.FileField(
        storage=MediaStorage(),
    )

    # Release website -Auto created
    release_website_url = models.CharField(max_length=100, null=True, blank=True)

    # Admin
    approved = models.BooleanField("Approved", default=False)
    comments = models.TextField(max_length=500, blank=True)

    # DB
    created_at = models.DateField(db_default=Now())
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # Methods
    def __str__(self):
        return self.release.release_title

    # Validations
    def clean(self):
        super().clean()
        validate_upload(self)

    def count_recipients(self):
        try:
            re = (self.recipients).split(",")
            return len(re)
        except Exception as e:
            raise {"Error while obtaining the e-mail addresses of the recipients.": {e}}

    def get_template(self):
        return self.template.url


# Pre save actions
@receiver(pre_save, sender=Campaign)
def create_release_website_url(sender, instance, **kwargs):
    if instance.pk is None:
        # Create website URL
        release_title = ((instance.release.release_title).lower()).replace(" ", "-")
        label_name = ((instance.label.label_name).lower()).replace(" ", "-")
        url = f"{release_title}-{label_name}-site"
        instance.release_website_url = url


# Post save actions
@receiver(post_save, sender=Campaign)
def post_save_methods(sender, instance, created, **kwargs):
    if created:
        # Create email template
        template = create_template(instance)
        instance.template = template
        instance.save()


# Remove files post delete
@receiver(post_delete, sender=Campaign)
def delete_file_after_deleted_obj(sender, instance, **kwargs):
    if instance.release_banner:
        instance.release_banner.delete(save=False)

    if instance.template:
        instance.template.delete(save=False)
