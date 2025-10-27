import boto3
from app.core import app_settings

s3_client = boto3.client(
    "s3",
    region_name=app_settings.aws_region,
    aws_access_key_id=app_settings.aws_access_key_id,
    aws_secret_access_key=app_settings.aws_secret_access_key,
)
