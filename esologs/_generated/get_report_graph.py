from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetReportGraph(BaseModel):
    report_data: Optional["GetReportGraphReportData"] = Field(alias="reportData")


class GetReportGraphReportData(BaseModel):
    report: Optional["GetReportGraphReportDataReport"]


class GetReportGraphReportDataReport(BaseModel):
    graph: Optional[Any]


GetReportGraph.model_rebuild()
GetReportGraphReportData.model_rebuild()
