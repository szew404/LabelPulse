from PIL import Image
from django.core.exceptions import ValidationError


def validate_upload(instance):
    # Label Logo
    if hasattr(instance, "label_logo") and instance.label_logo:
        img = Image.open(instance.label_logo)
        if img.width != 300 or img.height != 300:
            raise ValidationError("Image must be 300x300 pixels.")

        if not instance.label_logo.name.lower().endswith((".png")):
            raise ValidationError("Image must be in PNG format.")

    # Promotion Banner
    elif hasattr(instance, "release_banner") and instance.release_banner:
        img = Image.open(instance.release_banner)
        if img.width != 1200 or img.height != 400:
            raise ValidationError("Image must be 1200x400 pixels.")

        if not instance.release_banner.name.lower().endswith((".jpeg", ".jpg")):
            raise ValidationError("Image must be in JPG/JPEG format.")

    # Promotion Artwork
    elif hasattr(instance, "release_artwork") and instance.release_artwork:
        img = Image.open(instance.release_artwork)
        if img.width != 500 or img.height != 500:
            raise ValidationError("Image must be 500x500 pixels.")

        if not instance.release_artwork.name.lower().endswith((".jpeg", ".jpg")):
            raise ValidationError("Image must be in JPG/JPEG format.")

    # Promotion Track
    elif hasattr(instance, "track_file") and instance.track_file:
        if not instance.track_file.name.endswith(".mp3"):
            raise ValidationError("Tracks must be in MP3 format.")
