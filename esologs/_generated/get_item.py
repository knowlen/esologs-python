from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetItem(BaseModel):
    game_data: Optional["GetItemGameData"] = Field(alias="gameData")


class GetItemGameData(BaseModel):
    item: Optional["GetItemGameDataItem"]


class GetItemGameDataItem(BaseModel):
    id: int
    name: Optional[str]
    icon: Optional[str]


GetItem.model_rebuild()
GetItemGameData.model_rebuild()
