from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetGuilds(BaseModel):
    guild_data: Optional["GetGuildsGuildData"] = Field(alias="guildData")


class GetGuildsGuildData(BaseModel):
    guilds: Optional["GetGuildsGuildDataGuilds"]


class GetGuildsGuildDataGuilds(BaseModel):
    total: int
    per_page: int
    current_page: int
    from_: Optional[int] = Field(alias="from")
    to: Optional[int]
    last_page: int
    has_more_pages: bool
    data: Optional[List[Optional["GetGuildsGuildDataGuildsData"]]]


class GetGuildsGuildDataGuildsData(BaseModel):
    id: int
    name: str
    faction: "GetGuildsGuildDataGuildsDataFaction"
    server: "GetGuildsGuildDataGuildsDataServer"


class GetGuildsGuildDataGuildsDataFaction(BaseModel):
    name: str


class GetGuildsGuildDataGuildsDataServer(BaseModel):
    name: str
    region: "GetGuildsGuildDataGuildsDataServerRegion"


class GetGuildsGuildDataGuildsDataServerRegion(BaseModel):
    name: str


GetGuilds.model_rebuild()
GetGuildsGuildData.model_rebuild()
GetGuildsGuildDataGuilds.model_rebuild()
GetGuildsGuildDataGuildsData.model_rebuild()
GetGuildsGuildDataGuildsDataServer.model_rebuild()
