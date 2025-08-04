from typing import Any, List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetUserById(BaseModel):
    user_data: Optional["GetUserByIdUserData"] = Field(alias="userData")


class GetUserByIdUserData(BaseModel):
    user: Optional["GetUserByIdUserDataUser"]


class GetUserByIdUserDataUser(BaseModel):
    id: int
    name: str
    guilds: Optional[List[Optional["GetUserByIdUserDataUserGuilds"]]]
    characters: Optional[List[Optional["GetUserByIdUserDataUserCharacters"]]]
    na_display_name: Optional[str] = Field(alias="naDisplayName")
    eu_display_name: Optional[str] = Field(alias="euDisplayName")


class GetUserByIdUserDataUserGuilds(BaseModel):
    id: int
    name: str
    server: "GetUserByIdUserDataUserGuildsServer"


class GetUserByIdUserDataUserGuildsServer(BaseModel):
    name: str
    region: "GetUserByIdUserDataUserGuildsServerRegion"


class GetUserByIdUserDataUserGuildsServerRegion(BaseModel):
    name: str


class GetUserByIdUserDataUserCharacters(BaseModel):
    id: int
    name: str
    server: "GetUserByIdUserDataUserCharactersServer"
    game_data: Optional[Any] = Field(alias="gameData")
    class_id: int = Field(alias="classID")
    race_id: int = Field(alias="raceID")
    hidden: bool


class GetUserByIdUserDataUserCharactersServer(BaseModel):
    name: str
    region: "GetUserByIdUserDataUserCharactersServerRegion"


class GetUserByIdUserDataUserCharactersServerRegion(BaseModel):
    name: str


GetUserById.model_rebuild()
GetUserByIdUserData.model_rebuild()
GetUserByIdUserDataUser.model_rebuild()
GetUserByIdUserDataUserGuilds.model_rebuild()
GetUserByIdUserDataUserGuildsServer.model_rebuild()
GetUserByIdUserDataUserCharacters.model_rebuild()
GetUserByIdUserDataUserCharactersServer.model_rebuild()
