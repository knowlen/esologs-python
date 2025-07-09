from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetCharacterReports(BaseModel):
    character_data: Optional["GetCharacterReportsCharacterData"] = Field(
        alias="characterData"
    )


class GetCharacterReportsCharacterData(BaseModel):
    character: Optional["GetCharacterReportsCharacterDataCharacter"]


class GetCharacterReportsCharacterDataCharacter(BaseModel):
    recent_reports: Optional[
        "GetCharacterReportsCharacterDataCharacterRecentReports"
    ] = Field(alias="recentReports")


class GetCharacterReportsCharacterDataCharacterRecentReports(BaseModel):
    data: Optional[
        List[Optional["GetCharacterReportsCharacterDataCharacterRecentReportsData"]]
    ]
    total: int
    per_page: int
    current_page: int
    from_: Optional[int] = Field(alias="from")
    to: Optional[int]
    last_page: int
    has_more_pages: bool


class GetCharacterReportsCharacterDataCharacterRecentReportsData(BaseModel):
    code: str
    start_time: float = Field(alias="startTime")
    end_time: float = Field(alias="endTime")
    zone: Optional["GetCharacterReportsCharacterDataCharacterRecentReportsDataZone"]


class GetCharacterReportsCharacterDataCharacterRecentReportsDataZone(BaseModel):
    name: str


GetCharacterReports.model_rebuild()
GetCharacterReportsCharacterData.model_rebuild()
GetCharacterReportsCharacterDataCharacter.model_rebuild()
GetCharacterReportsCharacterDataCharacterRecentReports.model_rebuild()
GetCharacterReportsCharacterDataCharacterRecentReportsData.model_rebuild()
