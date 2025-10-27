from .dynamodb import friends_table
from .s3 import s3_client

__all__ = [
    "friends_table",
    "s3_client"
]