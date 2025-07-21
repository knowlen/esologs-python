from typing import Any, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetCharacterZoneRankings(BaseModel):
    character_data: Optional["GetCharacterZoneRankingsCharacterData"] = Field(
        alias="characterData"
    )


class GetCharacterZoneRankingsCharacterData(BaseModel):
    character: Optional["GetCharacterZoneRankingsCharacterDataCharacter"]


class GetCharacterZoneRankingsCharacterDataCharacter(BaseModel):
    zone_rankings: Optional[Any] = Field(alias="zoneRankings")


GetCharacterZoneRankings.model_rebuild()
GetCharacterZoneRankingsCharacterData.model_rebuild()
