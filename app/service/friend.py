import uuid

from fastapi import HTTPException

from app.core import app_settings
from app.db import s3_client
from app.schema import FriendObject, FriendResponseList


class FriendService:
    def __init__(self, table):
        self.table = table

    async def create_friend(self, data: FriendObject):
        item = data.model_dump()
        self.table.put_item(Item=item)
        return item

    async def get_friend(self, friend_id: str):
        response = self.table.get_item(
            Key={
                "id": friend_id,
            }
        )
        return response.get("Item")


    async def get_friends(self):
        response = self.table.scan()
        items = response.get("Items", [])
        return FriendResponseList(items=items)


    async def upload_photo(self, photo):
        if photo is not None:
            if photo.content_type not in ["image/jpeg", "image/png"]:
                raise HTTPException
            contents = await photo.read()
            if len(contents) > 10 * 1024 * 1024:
                raise HTTPException
        file_extension = photo.filename.split(".")[-1]
        file_key = f"friends/{uuid.uuid4()}.{file_extension}"

        s3_client.upload_fileobj(
            photo.file,
            app_settings.bucket_name,
            file_key,
            ExtraArgs={"ContentType": photo.content_type}
        )

        return f"https://{app_settings.bucket_name}.s3.eu-north-1.amazonaws.com/{file_key}"
