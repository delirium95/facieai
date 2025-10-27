import io
import uuid
from typing import Optional

from fastapi import APIRouter, UploadFile, Form, Depends
from openai import OpenAI
from starlette import status
from starlette.responses import StreamingResponse

from app.core.app_settings import app_settings
from app.db import s3_client
from app.dependencies import get_friend_service, get_llm_service
from app.schema import FriendObject
from app.schema.prompt import PromptRequest
from app.service import LlmService
from app.service.friend import FriendService

router = APIRouter(
    prefix='/friends'
)

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
)
async def create_friend(
    name: str = Form(...),
    profession: str = Form(...),
    profession_description: Optional[str] = Form(...),
    photo: UploadFile = Form(...),
    friend_service: FriendService = Depends(get_friend_service),
):
    photo_url = await friend_service.upload_photo(photo)

    friend_data = FriendObject(
        id=str(uuid.uuid4()),
        name=name,
        profession=profession,
        profession_description=profession_description,
        photo_url=photo_url
    )
    friend = await friend_service.create_friend(friend_data)
    return friend


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
)
async def get_friends(
        friend_service: FriendService = Depends(get_friend_service)
):
    return await friend_service.get_friends()


@router.get(
    '/{friend_id}',
    response_model=FriendObject,
    status_code=status.HTTP_200_OK,
)
async def get_friend(
        friend_id: str,
        friend_service: FriendService = Depends(get_friend_service)
):
    return await friend_service.get_friend(friend_id)


@router.get(
    "/media/{photo_key}",
    status_code=status.HTTP_200_OK,
)
async def get_media(photo_key: str):
    try:
        obj = s3_client.get_object(Bucket=app_settings.bucket_name, Key="friends/"+photo_key)
        return StreamingResponse(
            io.BytesIO(obj["Body"].read()),
            media_type=obj["ContentType"]
        )
    except s3_client.exceptions.NoSuchKey:
        return {"error": "File not found"}


@router.post(
    "/{friend_id}/ask"
)
async def generate_text(friend_id: str, llm_service: LlmService = Depends(get_llm_service),
                        friend_service: FriendService = Depends(get_friend_service)):
    return await llm_service.generate_response(friend_id, friend_service)
