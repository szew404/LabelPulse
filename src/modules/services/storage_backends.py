from django.conf import settings

import zipfile
import os
import io

import boto3
from botocore.client import Config
from botocore.exceptions import NoCredentialsError
from storages.backends.s3boto3 import S3Boto3Storage
from botocore.exceptions import ClientError


class MediaStorage(S3Boto3Storage):
    endpoint_url = "https://nyc3.digitaloceanspaces.com"
    location = "media"
    default_acl = "public-read"
    file_overwrite = False

    @property
    def querystring_auth(self):
        return False


# Session
def create_session():
    session = boto3.session.Session()

    client = session.client(
        "s3",
        region_name="nyc3",
        endpoint_url="https://nyc3.digitaloceanspaces.com",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    return client


# Upload HTML file to cloud
def save_template(filepath: str, html_content: str) -> dict:

    client = create_session()

    try:
        response = client.put_object(
            Bucket="cs.labelpulse",
            Key=f"media/{filepath}",
            Body=html_content,
            ACL="public-read",
            ContentType="text/html",
            Metadata={
                "x-amz-meta-s3cmd-attrs": "uid:1000/gname:asb/uname:asb/gid:1000/mode:33204/mtime:1499727909/atime:1499727909/md5:fb08934ef619f205f272b0adfd6c018c/ctime:1499713540",
            },
            StorageClass="STANDARD",
        )

        return {
            "detail": response,
            "message": f"File sent succesfully to Cloud.",
            "filepath": filepath,
        }
    except NoCredentialsError as e:
        return {
            "error": "Invalid credentials.",
            "detail": e,
        }


# Check if zip file exists
def get_zip_file(path: str, client):

    try:
        response = client.head_object(Bucket="cs.labelpulse", Key=f"media/{path}")
        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            return True
    except ClientError as e:
        return False

    return False


# Create and upload zip file
def create_zip_file(instance):

    client = create_session()

    zip_filename = f"{instance.release.artist}-{instance.release.release_title}.zip"
    label_path = str(instance.created_by.username)
    zip_path = f"tracks/{label_path}/{zip_filename}"

    # Chequeamos si existe
    if get_zip_file(zip_path, client):
        return f"media/{zip_path}"

    try:
        tracks = instance.release.get_tracks_listed()

        # Crear un archivo ZIP en memoria
        in_memory_zip = io.BytesIO()
        with zipfile.ZipFile(in_memory_zip, mode="w") as zip_file:
            for track in tracks:
                # Leer cada archivo de track y agregarlo al ZIP
                track_data = track.track_file.read()  # Leer el archivo
                zip_file.writestr(os.path.basename(track.track_file.name), track_data)

        # Una vez terminado, mover el puntero al inicio del archivo ZIP en memoria
        in_memory_zip.seek(0)

        response = client.put_object(
            Bucket="cs.labelpulse",
            Key=f"media/{zip_path}",
            Body=in_memory_zip,
            ACL="public-read",
            ContentType="application/zip",
            Metadata={
                "x-amz-meta-s3cmd-attrs": "uid:1000/gname:asb/uname:asb/gid:1000/mode:33204/mtime:1499727909/atime:1499727909/md5:fb08934ef619f205f272b0adfd6c018c/ctime:1499713540",
            },
            StorageClass="STANDARD",
        )

        return {
            "detail": response,
            "message": f"File sent succesfully to Cloud.",
            "filepath": f"media/{zip_path}",
        }

    except NoCredentialsError as e:
        return {
            "error": "Invalid credentials.",
            "detail": str(e),
        }

    except Exception as e:
        return {
            "error": "An error ocurred while creating the zip file.",
            "detail": str(e),
        }
