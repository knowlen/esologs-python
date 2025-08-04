from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetReportByCode(BaseModel):
    report_data: Optional["GetReportByCodeReportData"] = Field(alias="reportData")


class GetReportByCodeReportData(BaseModel):
    report: Optional["GetReportByCodeReportDataReport"]


class GetReportByCodeReportDataReport(BaseModel):
    code: str
    start_time: float = Field(alias="startTime")
    end_time: float = Field(alias="endTime")
    title: str
    visibility: str
    zone: Optional["GetReportByCodeReportDataReportZone"]
    fights: Optional[List[Optional["GetReportByCodeReportDataReportFights"]]]


class GetReportByCodeReportDataReportZone(BaseModel):
    name: str


class GetReportByCodeReportDataReportFights(BaseModel):
    id: int
    name: str
    difficulty: Optional[int]
    start_time: float = Field(alias="startTime")
    end_time: float = Field(alias="endTime")


GetReportByCode.model_rebuild()
GetReportByCodeReportData.model_rebuild()
GetReportByCodeReportDataReport.model_rebuild()
