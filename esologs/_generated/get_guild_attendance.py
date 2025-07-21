from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetGuildAttendance(BaseModel):
    guild_data: Optional["GetGuildAttendanceGuildData"] = Field(alias="guildData")


class GetGuildAttendanceGuildData(BaseModel):
    guild: Optional["GetGuildAttendanceGuildDataGuild"]


class GetGuildAttendanceGuildDataGuild(BaseModel):
    attendance: "GetGuildAttendanceGuildDataGuildAttendance"


class GetGuildAttendanceGuildDataGuildAttendance(BaseModel):
    total: int
    per_page: int
    current_page: int
    has_more_pages: bool
    data: Optional[List[Optional["GetGuildAttendanceGuildDataGuildAttendanceData"]]]


class GetGuildAttendanceGuildDataGuildAttendanceData(BaseModel):
    code: str
    start_time: Optional[float] = Field(alias="startTime")
    players: Optional[
        List[Optional["GetGuildAttendanceGuildDataGuildAttendanceDataPlayers"]]
    ]


class GetGuildAttendanceGuildDataGuildAttendanceDataPlayers(BaseModel):
    name: Optional[str]
    type: Optional[str]
    presence: Optional[int]


GetGuildAttendance.model_rebuild()
GetGuildAttendanceGuildData.model_rebuild()
GetGuildAttendanceGuildDataGuild.model_rebuild()
GetGuildAttendanceGuildDataGuildAttendance.model_rebuild()
GetGuildAttendanceGuildDataGuildAttendanceData.model_rebuild()
