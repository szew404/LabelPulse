from django.template.loader import render_to_string
from django.utils.text import slugify
from .storage_backends import save_template


def create_template(instance: object) -> str:

    filename = f"{slugify(instance.release.release_title)}-template.html"
    filepath = f"email-templates/{instance.created_by}/{filename}"

    context = {
        "title": instance.release.release_title,
        "type": instance.release.release_type,
        "online_version_url": f"media/{filepath}",
        "label_logo": instance.label.label_logo.url,
        "description": instance.release.release_description,
        "release_date": instance.release.release_date,
        "artist_name": instance.release.artist,
        "artwork": instance.release.release_artwork.url,
        "banner": instance.release_banner.url,
        "tracks": instance.release.get_tracks_listed,
        "label": instance.label,
        "release_website_url": f"website/{instance.release_website_url}",
    }

    html_content = render_to_string("campaigns/promo_template.html", context)

    try:
        save_template(filepath, html_content)
        return filepath
    except Exception as e:
        return print({"Error saving the template": e})


def render_template_for_email(instance: object) -> str:

    context = {
        "title": instance.release.release_title,
        "type": instance.release.release_type,
        "online_version_url": instance.template.url,
        "label_logo": instance.label.label_logo.url,
        "description": instance.release.release_description,
        "release_date": instance.release.release_date,
        "artist_name": instance.release.artist,
        "artwork": instance.release.release_artwork.url,
        "banner": instance.release_banner.url,
        "tracks": instance.release.get_tracks_listed,
        "label": instance.label,
        "release_website_url": f"website/{instance.release_website_url}",
    }

    return render_to_string("campaigns/promo_template.html", context)
