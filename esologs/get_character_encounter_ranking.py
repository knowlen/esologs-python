from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetCharacterEncounterRanking(BaseModel):
    character_data: Optional["GetCharacterEncounterRankingCharacterData"] = Field(
        alias="characterData"
    )


class GetCharacterEncounterRankingCharacterData(BaseModel):
    character: Optional["GetCharacterEncounterRankingCharacterDataCharacter"]


class GetCharacterEncounterRankingCharacterDataCharacter(BaseModel):
    encounter_rankings: Optional[Any] = Field(alias="encounterRankings")


GetCharacterEncounterRanking.model_rebuild()
GetCharacterEncounterRankingCharacterData.model_rebuild()
