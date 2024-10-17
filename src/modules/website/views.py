from django.shortcuts import render
from django import http
from django.http import HttpResponseRedirect
from django.views.decorators.clickjacking import xframe_options_exempt

from modules.campaigns.models import Campaign
from modules.services.storage_backends import create_zip_file


@xframe_options_exempt
def downloads(request, release_website_url):

    try:
        campaign = Campaign.objects.get(release_website_url=release_website_url)
    except Campaign.DoesNotExist:
        raise http.Http404("Campaign not found")

    if request.GET.get("download") == "zip":
        zip_file_path = create_zip_file(campaign)
        return HttpResponseRedirect(zip_file_path.get("filepath", None))

    context = {
        "banner": campaign.release_banner.url,
        "title": campaign.release.release_title,
        "type": campaign.release.release_type,
        "artist_name": campaign.release.artist,
        "download_all_url": f"{request.path}?download=zip",
        "tracks": campaign.release.get_tracks_listed,
        "description": campaign.release.release_description,
        "label": campaign.label,
        "artwork": campaign.release.release_artwork.url,
        "link_1": campaign.label.link_1,
        "link_1_name": campaign.label.link_1_name,
        "link_2": campaign.label.link_2,
        "link_2_name": campaign.label.link_2_name,
    }

    return render(request, "website/download.html", context)
