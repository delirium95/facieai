import boto3
from app.core import app_settings


dynamodb = boto3.resource(
    'dynamodb',
    region_name=app_settings.aws_region,
    endpoint_url=app_settings.aws_endpoint,
    aws_access_key_id=app_settings.aws_access_key_id,
    aws_secret_access_key=app_settings.aws_secret_access_key,
)

friends_table = dynamodb.Table('friends')
