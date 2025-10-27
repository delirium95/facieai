from pydantic import Field

from app.core.config_base import ConfigBase


class AppSettings(ConfigBase):
    host: str = Field("127.0.0.1", alias="HOST")
    port: int = Field(8000, alias="PORT")

    bucket_name: str = Field(None, alias="BUCKET_NAME")

    aws_access_key_id: str = Field(None, alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(None, alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(None, alias="AWS_REGION")
    aws_endpoint: str = Field(None, alias="AWS_ENDPOINT")

    open_ai_key: str = Field(None, alias="OPEN_AI_KEY")


app_settings = AppSettings()
