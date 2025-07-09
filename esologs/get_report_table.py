from typing import Any, Optional

from pydantic import Field

from .base_model import BaseModel


class GetReportTable(BaseModel):
    report_data: Optional["GetReportTableReportData"] = Field(alias="reportData")


class GetReportTableReportData(BaseModel):
    report: Optional["GetReportTableReportDataReport"]


class GetReportTableReportDataReport(BaseModel):
    table: Optional[Any]


GetReportTable.model_rebuild()
GetReportTableReportData.model_rebuild()
