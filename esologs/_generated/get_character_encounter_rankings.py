from typing import Any, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetCharacterEncounterRankings(BaseModel):
    character_data: Optional["GetCharacterEncounterRankingsCharacterData"] = Field(
        alias="characterData"
    )


class GetCharacterEncounterRankingsCharacterData(BaseModel):
    character: Optional["GetCharacterEncounterRankingsCharacterDataCharacter"]


class GetCharacterEncounterRankingsCharacterDataCharacter(BaseModel):
    encounter_rankings: Optional[Any] = Field(alias="encounterRankings")


GetCharacterEncounterRankings.model_rebuild()
GetCharacterEncounterRankingsCharacterData.model_rebuild()
