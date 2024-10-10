from django.template.loader import render_to_string
from django.conf import settings
from django.utils.text import slugify
from .storage_backends import save_template


def create_template(instance: object) -> str:

    context = {
        "title": instance.release.release_title,
        "type": instance.release.release_type,
        "description": instance.release.release_description,
        "artist_name": instance.release.artist,
        "banner": instance.release_banner.url,
        "artwork": instance.release.release_artwork.url,
        "tracks": instance.release.get_tracks_listed,
        "label": instance.label,
        "release_website_url": f"website/{instance.release_website_url}",
    }

    html_content = render_to_string("campaigns/promo_template.html", context)

    filename = f"{slugify(instance.release.release_title)}-template.html"
    filepath = f"email-templates/{instance.created_by}/{filename}"

    try:
        save_template(filepath, html_content)
        return filepath
    except Exception as e:
        return print({"Error saving the template": e})


def render_template_for_email(instance: object) -> str:

    context = {
        "title": instance.release.release_title,
        "type": instance.release.release_type,
        "description": instance.release.release_description,
        "artist_name": instance.release.artist,
        "banner": instance.release_banner.url,
        "artwork": instance.release.release_artwork.url,
        "tracks": instance.release.get_tracks_listed,
        "label": instance.label,
        "release_website_url": f"website/{instance.release_website_url}",
    }

    return render_to_string("campaigns/promo_template.html", context)
