from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetCurrentUser(BaseModel):
    user_data: Optional["GetCurrentUserUserData"] = Field(alias="userData")


class GetCurrentUserUserData(BaseModel):
    current_user: Optional["GetCurrentUserUserDataCurrentUser"] = Field(
        alias="currentUser"
    )


class GetCurrentUserUserDataCurrentUser(BaseModel):
    id: int
    name: str
    guilds: Optional[List[Optional["GetCurrentUserUserDataCurrentUserGuilds"]]]
    characters: Optional[List[Optional["GetCurrentUserUserDataCurrentUserCharacters"]]]
    na_display_name: Optional[str] = Field(alias="naDisplayName")
    eu_display_name: Optional[str] = Field(alias="euDisplayName")


class GetCurrentUserUserDataCurrentUserGuilds(BaseModel):
    id: int
    name: str
    server: "GetCurrentUserUserDataCurrentUserGuildsServer"


class GetCurrentUserUserDataCurrentUserGuildsServer(BaseModel):
    name: str
    region: "GetCurrentUserUserDataCurrentUserGuildsServerRegion"


class GetCurrentUserUserDataCurrentUserGuildsServerRegion(BaseModel):
    name: str


class GetCurrentUserUserDataCurrentUserCharacters(BaseModel):
    id: int
    name: str
    server: "GetCurrentUserUserDataCurrentUserCharactersServer"
    game_data: Optional[Any] = Field(alias="gameData")
    class_id: int = Field(alias="classID")
    race_id: int = Field(alias="raceID")
    hidden: bool


class GetCurrentUserUserDataCurrentUserCharactersServer(BaseModel):
    name: str
    region: "GetCurrentUserUserDataCurrentUserCharactersServerRegion"


class GetCurrentUserUserDataCurrentUserCharactersServerRegion(BaseModel):
    name: str


GetCurrentUser.model_rebuild()
GetCurrentUserUserData.model_rebuild()
GetCurrentUserUserDataCurrentUser.model_rebuild()
GetCurrentUserUserDataCurrentUserGuilds.model_rebuild()
GetCurrentUserUserDataCurrentUserGuildsServer.model_rebuild()
GetCurrentUserUserDataCurrentUserCharacters.model_rebuild()
GetCurrentUserUserDataCurrentUserCharactersServer.model_rebuild()
