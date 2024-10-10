from django.urls import path
from .views import downloads

urlpatterns = [
    path("<str:release_website_url>/downloads/", downloads, name="downloads"),
]
