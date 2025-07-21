from typing import List, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetGuildMembers(BaseModel):
    guild_data: Optional["GetGuildMembersGuildData"] = Field(alias="guildData")


class GetGuildMembersGuildData(BaseModel):
    guild: Optional["GetGuildMembersGuildDataGuild"]


class GetGuildMembersGuildDataGuild(BaseModel):
    members: "GetGuildMembersGuildDataGuildMembers"


class GetGuildMembersGuildDataGuildMembers(BaseModel):
    total: int
    per_page: int
    current_page: int
    has_more_pages: bool
    data: Optional[List[Optional["GetGuildMembersGuildDataGuildMembersData"]]]


class GetGuildMembersGuildDataGuildMembersData(BaseModel):
    id: int
    name: str
    server: "GetGuildMembersGuildDataGuildMembersDataServer"
    guild_rank: int = Field(alias="guildRank")


class GetGuildMembersGuildDataGuildMembersDataServer(BaseModel):
    name: str
    region: "GetGuildMembersGuildDataGuildMembersDataServerRegion"


class GetGuildMembersGuildDataGuildMembersDataServerRegion(BaseModel):
    name: str


GetGuildMembers.model_rebuild()
GetGuildMembersGuildData.model_rebuild()
GetGuildMembersGuildDataGuild.model_rebuild()
GetGuildMembersGuildDataGuildMembers.model_rebuild()
GetGuildMembersGuildDataGuildMembersData.model_rebuild()
GetGuildMembersGuildDataGuildMembersDataServer.model_rebuild()
