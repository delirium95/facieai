from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class FriendCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field()
    profession: str = Field()
    profession_description: Optional[str] = Field(None)
    photo_url: Optional[str] = Field(None)


class FriendObject(FriendCreate):
    model_config = ConfigDict(from_attributes=True)
    id: str = Field()


class FriendResponseList(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    items: List[FriendObject]
