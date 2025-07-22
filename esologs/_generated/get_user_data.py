from typing import Optional

from pydantic import Field

from .base_model import BaseModel


class GetUserData(BaseModel):
    user_data: Optional["GetUserDataUserData"] = Field(alias="userData")


class GetUserDataUserData(BaseModel):
    user: Optional["GetUserDataUserDataUser"]


class GetUserDataUserDataUser(BaseModel):
    id: int


GetUserData.model_rebuild()
GetUserDataUserData.model_rebuild()
