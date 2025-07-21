from typing import Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetClass(BaseModel):
    game_data: Optional["GetClassGameData"] = Field(alias="gameData")


class GetClassGameData(BaseModel):
    class_: Optional["GetClassGameDataClass"] = Field(alias="class")


class GetClassGameDataClass(BaseModel):
    id: int
    name: str
    slug: str


GetClass.model_rebuild()
GetClassGameData.model_rebuild()
