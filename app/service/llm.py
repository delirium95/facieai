from http.client import HTTPException

from openai import AsyncOpenAI
from starlette import status

from app.core import app_settings
from app.util import ModelDoesNotExist


class LlmService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=app_settings.open_ai_key)

    async def generate_response(self, friend_id: str, friend_service):
        friend = await friend_service.get_friend(friend_id)
        if not friend:
            raise ModelDoesNotExist
        profession = friend.get("profession")
        if not profession:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Profession not found")
        profession_description = friend.get("profession_description")
        if not profession_description:
            question = f"Які основні проблеми у професії {profession}?"
        else:
            question = f"Які основні проблеми у професії {profession}? Її опис: {profession_description}"
        try:
            response = await self.client.chat.completions.create(
                model="gpt-5-nano",
                messages=[
                    {"role": "user", "content": question}
                ],
                max_tokens=200
            )
            return {"generated_text": response.choices[0].message.content}
        except Exception as e:
            return {"answer": f"(mock) У цій професії головні труднощі пов’язані зі стресом і конкуренцією. ({e})"}
