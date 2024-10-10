import os
from django.utils.text import slugify


def upload_path(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)

    # Label logo
    if hasattr(instance, "label_logo") and instance.label_logo:
        return f"logos/{instance.created_by}/{slugify(instance.label_name)}-Logo{filename_ext}"

    # Release artwork
    elif hasattr(instance, "release_artwork") and instance.release_artwork:
        return f"artworks/{instance.created_by}/{slugify(instance.release_title)}-Artwork{filename_ext}"

    # Track file
    elif hasattr(instance, "track_file") and instance.track_file:
        return f"tracks/{instance.created_by}/{slugify(instance.track_artist)}-{slugify(instance.track_title)}{filename_ext}"

    # Campaign release banner
    elif hasattr(instance, "release_banner") and instance.release_banner:
        return f"banners/{instance.created_by}/{slugify(instance.release.release_title)}-Banner{filename_ext}"
