from typing import Any, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetReportRankings(BaseModel):
    report_data: Optional["GetReportRankingsReportData"] = Field(alias="reportData")


class GetReportRankingsReportData(BaseModel):
    report: Optional["GetReportRankingsReportDataReport"]


class GetReportRankingsReportDataReport(BaseModel):
    rankings: Optional[Any]


GetReportRankings.model_rebuild()
GetReportRankingsReportData.model_rebuild()
