from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetProgressRace(BaseModel):
    progress_race_data: Optional["GetProgressRaceProgressRaceData"] = Field(
        alias="progressRaceData"
    )


class GetProgressRaceProgressRaceData(BaseModel):
    progress_race: Optional[Any] = Field(alias="progressRace")


GetProgressRace.model_rebuild()
