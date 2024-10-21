from django.contrib import admin
from .models import Label, Release, Track
from django.utils.html import format_html


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):

    # Utils
    def created_by_name(self, obj):
        return obj.created_by.first_name + " " + obj.created_by.last_name

    created_by_name.short_description = "Created By"

    def release_name(self, obj):
        release = Release.objects.get(tracks=obj)
        return release

    # Model config
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user).distinct()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # Management
    ordering = ["track_artist"]
    search_fields = ["track_title"]

    # Visualisation
    list_display = [
        "track_title",
        "track_artist",
        "release_name",
        "track_genre",
        "created_by_name",
    ]

    list_select_related = True

    list_per_page = 5

    # Create
    fieldsets = [
        (
            "Track Information",
            {
                "fields": (
                    "track_title",
                    "track_artist",
                    "track_genre",
                    "track_style",
                )
            },
        ),
        (
            "Settings & Track File",
            {
                "fields": (
                    "play_from",
                    "track_file",
                )
            },
        ),
    ]


@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):

    # Utils
    def tracks_number(self, obj):
        return Release.count_tracks(obj)

    tracks_number.short_description = "Tracks"

    def render_artwork(self, obj):
        if obj.release_artwork:
            # Add a template for this
            return format_html(
                '<div style="text-align: center;"><img src="{}" style="max-width: 90px; max-height: 90px;"/></div>',
                obj.release_artwork.url,
            )
        return "No Image"

    render_artwork.short_description = "Artwork"

    # Model config
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user).distinct()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tracks":
            if not request.user.is_superuser:
                kwargs["queryset"] = Track.objects.filter(created_by=request.user)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def had_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.created_by == request.user
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.save()

        # Add release to the label
        label = Label.objects.get(created_by=request.user)
        label.releases.add(obj)
        label.save()

        super().save_model(request, obj, form, change)

    # Management
    ordering = ["release_title"]
    search_fields = ["release_title", "artist"]

    # Visualisation
    list_display = [
        "render_artwork",
        "release_title",
        "release_type",
        "artist",
        "release_date",
        "tracks_number",
    ]

    list_per_page = 5

    list_select_related = True

    list_display_links = [
        "release_title",
    ]

    # Create
    fieldsets = [
        (
            "Release Information",
            {
                "fields": (
                    "release_title",
                    "release_date",
                    "release_type",
                    "release_description",
                )
            },
        ),
        (
            "Artists & Tracks",
            {
                "fields": (
                    "artist",
                    "included_artists",
                    "tracks",
                )
            },
        ),
        (
            "Artwork",
            {"fields": ("release_artwork",)},
        ),
    ]


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):

    # Utils
    def created_by_name(self, obj):
        return obj.legal_first_name + " " + obj.legal_last_name

    created_by_name.short_description = "Owner Full Name"

    # Permissions
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def had_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser:
            return obj.label.created_by == request.user
        return super().has_change_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        if Label.objects.filter(created_by=request.user).exists():
            return False
        return True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    # Management
    ordering = ["label_name"]
    search_fields = ["label_name", "genre"]

    # Visualisation
    list_display = [
        "label_name",
        "genre",
        "points",
        "created_by_name",
    ]

    # Create
    fieldsets = [
        (
            "Label Information",
            {
                "fields": (
                    "label_name",
                    "country",
                    "genre",
                    "style",
                    "birth_date",
                )
            },
        ),
        (
            "Legal Information",
            {
                "fields": (
                    "legal_first_name",
                    "legal_last_name",
                    "legal_email",
                    "legal_country",
                    "legal_city",
                    "legal_address",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "label_email",
                    "phone_number",
                    "label_logo",
                )
            },
        ),
        (
            "Social Media Links",
            {
                "fields": (
                    "link_1",
                    "link_1_name",
                    "link_2",
                    "link_2_name",
                )
            },
        ),
    ]

    # Exclude fields
    exclude = [
        "releases",
        "points",
        "created_at",
        "created_by",
    ]
