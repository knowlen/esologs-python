from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetFactions(BaseModel):
    game_data: Optional["GetFactionsGameData"] = Field(alias="gameData")


class GetFactionsGameData(BaseModel):
    factions: Optional[List[Optional["GetFactionsGameDataFactions"]]]


class GetFactionsGameDataFactions(BaseModel):
    id: int
    name: str


GetFactions.model_rebuild()
GetFactionsGameData.model_rebuild()
