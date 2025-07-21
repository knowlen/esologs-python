from typing import Any, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetReportPlayerDetails(BaseModel):
    report_data: Optional["GetReportPlayerDetailsReportData"] = Field(
        alias="reportData"
    )


class GetReportPlayerDetailsReportData(BaseModel):
    report: Optional["GetReportPlayerDetailsReportDataReport"]


class GetReportPlayerDetailsReportDataReport(BaseModel):
    player_details: Optional[Any] = Field(alias="playerDetails")


GetReportPlayerDetails.model_rebuild()
GetReportPlayerDetailsReportData.model_rebuild()
