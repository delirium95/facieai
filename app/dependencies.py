from app.db.dynamodb import friends_table
from app.service import LlmService
from app.service.friend import FriendService


async def get_friend_service():
    yield FriendService(friends_table)


async def get_llm_service():
    yield LlmService()