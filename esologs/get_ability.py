from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetAbility(BaseModel):
    game_data: Optional["GetAbilityGameData"] = Field(alias="gameData")


class GetAbilityGameData(BaseModel):
    ability: Optional["GetAbilityGameDataAbility"]


class GetAbilityGameDataAbility(BaseModel):
    id: int
    name: Optional[str]
    icon: Optional[str]
    description: Optional[str]


GetAbility.model_rebuild()
GetAbilityGameData.model_rebuild()
