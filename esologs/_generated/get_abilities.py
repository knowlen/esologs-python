from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetAbilities(BaseModel):
    game_data: Optional["GetAbilitiesGameData"] = Field(alias="gameData")


class GetAbilitiesGameData(BaseModel):
    abilities: Optional["GetAbilitiesGameDataAbilities"]


class GetAbilitiesGameDataAbilities(BaseModel):
    data: Optional[List[Optional["GetAbilitiesGameDataAbilitiesData"]]]
    total: int
    per_page: int
    current_page: int
    from_: Optional[int] = Field(alias="from")
    to: Optional[int]
    last_page: int
    has_more_pages: bool


class GetAbilitiesGameDataAbilitiesData(BaseModel):
    id: int
    name: Optional[str]
    icon: Optional[str]


GetAbilities.model_rebuild()
GetAbilitiesGameData.model_rebuild()
GetAbilitiesGameDataAbilities.model_rebuild()
