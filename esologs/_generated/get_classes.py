from typing import List, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetClasses(BaseModel):
    game_data: Optional["GetClassesGameData"] = Field(alias="gameData")


class GetClassesGameData(BaseModel):
    classes: Optional[List[Optional["GetClassesGameDataClasses"]]]


class GetClassesGameDataClasses(BaseModel):
    id: int
    name: str
    slug: str


GetClasses.model_rebuild()
GetClassesGameData.model_rebuild()
