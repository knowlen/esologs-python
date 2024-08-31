from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetMap(BaseModel):
    game_data: Optional["GetMapGameData"] = Field(alias="gameData")


class GetMapGameData(BaseModel):
    map: Optional["GetMapGameDataMap"]


class GetMapGameDataMap(BaseModel):
    id: int
    name: Optional[str]


GetMap.model_rebuild()
GetMapGameData.model_rebuild()
