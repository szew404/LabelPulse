from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.files.storage import default_storage

from unfold.admin import ModelAdmin

from .models import Campaign
from modules.labels.models import Release, Label


@admin.register(Campaign)
class CampaignAdmin(ModelAdmin):

    # Management
    ordering = ["release"]
    search_fields = ["release"]

    # Visualisation
    list_display = [
        "release",
        "sent_date",
        "campaign_sent",
        "send_test_email_button",
        "get_template",
        "get_website",
        "approved",
        "comments",
    ]

    list_select_related = True

    list_per_page = 5

    # Create
    fieldsets = [
        (
            "Campaign Information",
            {
                "fields": (
                    "release",
                    "release_banner",
                    "sent_date",
                    "recipients",
                    "test_email_address",
                )
            },
        ),
    ]

    # Model config
    def get_queryset(self, request):

        if self.fieldsets is None:
            self.fieldsets = []

        mngmt = (
            "Management",
            {
                "fields": (
                    "approved",
                    "comments",
                    "release_website_url",
                ),
            },
        )

        if request.user.is_superuser and mngmt not in self.fieldsets:
            self.fieldsets.append(mngmt)

        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "release":
            if not request.user.is_superuser:
                kwargs["queryset"] = Release.objects.filter(created_by=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def had_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.created_by == request.user
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

            # Get the user label
            label = Label.objects.filter(created_by=request.user).first()

            if label:
                obj.label = label
            else:
                self.message_user(
                    request=request,
                    message="Not possible to create the campaign: You doesn't have a record label registered.",
                    level=messages.ERROR,
                )
                return

        if change:
            old_obj = Campaign.objects.get(pk=obj.pk)
            if old_obj.banner_release != obj.banner_release:

                if old_obj.banner_release:
                    default_storage.delete(old_obj.banner_release.name)

        super().save_model(request, obj, form, change)

    # Utils
    def send_test_email_button(self, obj):
        if obj.test_email_address:
            send_url = reverse("send_test_email", args=[obj.id])
            button = render_to_string(
                "campaigns/send_test_button.html", {"url": send_url}
            )

            return format_html(button)

        return "No test email address available"

    send_test_email_button.short_description = "Test your campaign"

    def get_template(self, obj):
        if obj.template:
            template_url = obj.template.url
            button = render_to_string(
                "campaigns/view_template_button.html", {"template_url": template_url}
            )

            return format_html(button)
        return "No Template Available"

    get_template.short_description = "Email Template"

    def get_website(self, obj):
        if obj.release_website_url:
            website_url = (
                f"https://label-pulse.com/website/{obj.release_website_url}/downloads/"
            )
            button = render_to_string(
                "campaigns/view_website_button.html", {"website_url": website_url}
            )

            return format_html(button)
        return "No Web Available"

    get_website.short_description = "Release Website"
