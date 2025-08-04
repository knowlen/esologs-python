from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetNPCs(BaseModel):
    game_data: Optional["GetNPCsGameData"] = Field(alias="gameData")


class GetNPCsGameData(BaseModel):
    npcs: Optional["GetNPCsGameDataNpcs"]


class GetNPCsGameDataNpcs(BaseModel):
    data: Optional[List[Optional["GetNPCsGameDataNpcsData"]]]
    total: int
    per_page: int
    current_page: int
    from_: Optional[int] = Field(alias="from")
    to: Optional[int]
    last_page: int
    has_more_pages: bool


class GetNPCsGameDataNpcsData(BaseModel):
    id: int
    name: Optional[str]


GetNPCs.model_rebuild()
GetNPCsGameData.model_rebuild()
GetNPCsGameDataNpcs.model_rebuild()
