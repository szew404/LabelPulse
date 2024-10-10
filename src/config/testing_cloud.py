import boto3
from botocore.client import Config
import decouple

# Env config
DOTENV_FILE = "src/config/.env"
env_config = decouple.Config(decouple.RepositoryEnv(DOTENV_FILE))


# Initialize a session using DigitalOcean Spaces.
session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="nyc3",
    endpoint_url="https://nyc3.digitaloceanspaces.com",
    aws_access_key_id=env_config.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=env_config.get("AWS_SECRET_ACCESS_KEY"),
)

# List all buckets on your account.
response = client.list_buckets()
spaces = [space["Name"] for space in response["Buckets"]]
print("Spaces List: %s" % spaces)
