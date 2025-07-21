from typing import Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetRateLimitData(BaseModel):
    rate_limit_data: Optional["GetRateLimitDataRateLimitData"] = Field(
        alias="rateLimitData"
    )


class GetRateLimitDataRateLimitData(BaseModel):
    limit_per_hour: int = Field(alias="limitPerHour")
    points_spent_this_hour: float = Field(alias="pointsSpentThisHour")
    points_reset_in: int = Field(alias="pointsResetIn")


GetRateLimitData.model_rebuild()
