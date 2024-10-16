from django.db import models
from django.db.models.functions import Now
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver

from modules.services.storage_backends import MediaStorage

from utils import (
    GENRES_CHOICES,
    STYLES_CHOICES,
    validate_upload,
    upload_path,
)


class Track(models.Model):

    # Track Information
    track_title = models.CharField(max_length=100)
    track_artist = models.CharField(max_length=100)
    track_genre = models.CharField(
        max_length=100,
        choices=GENRES_CHOICES,
        blank=False,
        null=False,
    )
    track_style = models.CharField(
        max_length=100,
        choices=STYLES_CHOICES,
        blank=False,
        null=False,
    )

    # Set up
    play_from = models.CharField(
        max_length=5,
        blank=True,
        help_text="Start of playback of the track in the publication of the Promotion. Example: 01:20",
    )

    # File
    track_file = models.FileField(
        upload_to=upload_path,
        storage=MediaStorage(),
        help_text="Track format permitted: MP3",
    )

    # DB
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(db_default=Now())

    def __str__(self):
        return self.track_artist + " - " + self.track_title

    # Validations
    def clean(self):
        super().clean()
        validate_upload(self)

    # Download track file URL
    @property
    def download_url(self):
        if self.track_file:
            return self.track_file.url
        return None

    class Meta:
        verbose_name = "Track"
        verbose_name_plural = "Tracks"


"""# Change the name of the track file to: artist name - track title
@receiver(post_save, sender=Track)
def rename_track_file(sender, instance, created, **kwargs):
    if created:
        new_title = clean_file_name(instance)
        instance.track_file.name = new_title
        instance.save()"""


# Remove the file post delete
@receiver(post_delete, sender=Track)
def delete_file_after_deleted_obj(sender, instance, **kwargs):
    if instance.track_file:
        instance.track_file.delete(save=False)


class Release(models.Model):

    # Information
    release_title = models.CharField(
        help_text="Do not include Artists, EP, Album, Etc",
        max_length=200,
        blank=False,
        null=False,
    )
    release_date = models.DateField(
        blank=False,
        null=False,
        help_text="Date of when the release will be published",
    )

    RLSD_CHOICES = [
        ("EP", "EP"),
        ("Album", "Album"),
        ("Single", "Single"),
    ]
    release_type = models.CharField(max_length=50, choices=RLSD_CHOICES)

    release_description = models.TextField(
        max_length=1000,
        help_text="1000 Characters max. Do not include tracklist or social media links.",
    )

    artist = models.CharField(max_length=100, blank=False, null=False)
    included_artists = models.TextField(
        max_length=500,
        blank=True,
        help_text="Add multiple artists separated by commas",
    )

    # Relase's tracks
    tracks = models.ManyToManyField(Track, related_name="releases_tracks", blank=True)

    # Design
    release_artwork = models.ImageField(
        upload_to=upload_path,
        storage=MediaStorage(),
        help_text="This image will appear on the promotional email.",
        default="media/default-images/label-logo-default.png",
    )

    # DB
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(db_default=Now())

    class Meta:
        verbose_name = "Release"
        verbose_name_plural = "Releases"

    # Validations
    def clean(self):
        super().clean()
        validate_upload(self)

    # Methods
    def __str__(self):
        return self.release_title + " " + self.release_type

    def get_tracks_listed(self):
        return list(self.tracks.all())

    def count_tracks(self):
        return self.tracks.count()


"""# Change the name of the artwork file to: Release Title - Artwork
@receiver(post_save, sender=Release)
def rename_artwork_file(sender, instance, created, **kwargs):
    if created:
        new_title = clean_file_name(instance)
        instance.release_artwork.name = new_title
        instance.save()"""


# Remove the file post delete
@receiver(post_delete, sender=Release)
def delete_file_after_deleted_obj(sender, instance, **kwargs):
    if instance.release_artwork:
        instance.release_artwork.delete(save=False)


class Label(models.Model):

    # Label Information
    label_name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    country = models.CharField(max_length=100, blank=False, null=False)
    genre = models.CharField(
        max_length=100, choices=GENRES_CHOICES, blank=False, null=False
    )
    style = models.CharField(
        max_length=100, choices=STYLES_CHOICES, blank=False, null=False
    )
    birth_date = models.DateField(blank=False, null=False)
    label_logo = models.ImageField(
        upload_to=upload_path,
        storage=MediaStorage(),
        help_text="This logo will appear on the promotional email. Width & Height: 300px. File format permited: PNG",
        default="default-images/label-logo-default.png",
    )

    # Releases Information
    releases = models.ManyToManyField(
        Release, related_name="labels_releases", blank=True
    )
    points = models.IntegerField(default=0)

    # Legal Information
    legal_first_name = models.CharField(max_length=100, blank=False, null=False)
    legal_last_name = models.CharField(max_length=100, blank=False, null=False)
    legal_email = models.EmailField(blank=False, null=False)
    legal_country = models.CharField(max_length=100, blank=False, null=False)
    legal_city = models.CharField(max_length=100, blank=False, null=False)
    legal_address = models.CharField(max_length=100, blank=False, null=False)

    # Contact Information
    label_email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.TextField(blank=False, null=False)

    # Social Media Links
    link_1 = models.URLField("Social Media Link 1", blank=False, null=True)
    link_1_name = models.CharField("Link name", max_length=50, blank=False, null=True)

    link_2 = models.URLField("Social Media Link 2", blank=False, null=True)
    link_2_name = models.CharField("Link name", max_length=50, blank=False, null=True)

    # DB
    created_at = models.DateField(db_default=Now())
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "My Label"
        verbose_name_plural = "My Label"

    def __str__(self):
        return self.label_name

    # Validations
    def clean(self):
        super().clean()
        validate_upload(self)


"""# Change the name of the logo file to: Label Name - Logo
@receiver(pre_save, sender=Label)
def rename_logo_file(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Label.objects.get(pk=instance.pk)
        if old_instance.label_logo != instance.label_logo:
            filename = f"{instance.label_name}-Logo.png"
            instance.label_logo.name = filename
    else:
        filename = f"{instance.label_name}-Logo.png"
        instance.label_logo.name = filename"""


# Remove the file post delete
@receiver(post_delete, sender=Label)
def delete_file_after_deleted_obj(sender, instance, **kwargs):
    if instance.label_logo:
        instance.label_logo.delete(save=False)
