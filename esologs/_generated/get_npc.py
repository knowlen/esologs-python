from typing import Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetNPC(BaseModel):
    game_data: Optional["GetNPCGameData"] = Field(alias="gameData")


class GetNPCGameData(BaseModel):
    npc: Optional["GetNPCGameDataNpc"]


class GetNPCGameDataNpc(BaseModel):
    id: int
    name: Optional[str]


GetNPC.model_rebuild()
GetNPCGameData.model_rebuild()
