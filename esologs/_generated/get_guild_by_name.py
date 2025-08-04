from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetGuildByName(BaseModel):
    guild_data: Optional["GetGuildByNameGuildData"] = Field(alias="guildData")


class GetGuildByNameGuildData(BaseModel):
    guild: Optional["GetGuildByNameGuildDataGuild"]


class GetGuildByNameGuildDataGuild(BaseModel):
    id: int
    name: str
    description: str
    faction: "GetGuildByNameGuildDataGuildFaction"
    server: "GetGuildByNameGuildDataGuildServer"
    tags: Optional[List[Optional["GetGuildByNameGuildDataGuildTags"]]]


class GetGuildByNameGuildDataGuildFaction(BaseModel):
    name: str


class GetGuildByNameGuildDataGuildServer(BaseModel):
    name: str
    region: "GetGuildByNameGuildDataGuildServerRegion"


class GetGuildByNameGuildDataGuildServerRegion(BaseModel):
    name: str


class GetGuildByNameGuildDataGuildTags(BaseModel):
    id: int
    name: str


GetGuildByName.model_rebuild()
GetGuildByNameGuildData.model_rebuild()
GetGuildByNameGuildDataGuild.model_rebuild()
GetGuildByNameGuildDataGuildServer.model_rebuild()
