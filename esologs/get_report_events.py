from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetReportEvents(BaseModel):
    report_data: Optional["GetReportEventsReportData"] = Field(alias="reportData")


class GetReportEventsReportData(BaseModel):
    report: Optional["GetReportEventsReportDataReport"]


class GetReportEventsReportDataReport(BaseModel):
    events: Optional["GetReportEventsReportDataReportEvents"]


class GetReportEventsReportDataReportEvents(BaseModel):
    data: Optional[Any]
    next_page_timestamp: Optional[float] = Field(alias="nextPageTimestamp")


GetReportEvents.model_rebuild()
GetReportEventsReportData.model_rebuild()
GetReportEventsReportDataReport.model_rebuild()
