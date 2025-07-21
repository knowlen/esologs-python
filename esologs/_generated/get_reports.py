from typing import List, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetReports(BaseModel):
    report_data: Optional["GetReportsReportData"] = Field(alias="reportData")


class GetReportsReportData(BaseModel):
    reports: Optional["GetReportsReportDataReports"]


class GetReportsReportDataReports(BaseModel):
    data: Optional[List[Optional["GetReportsReportDataReportsData"]]]
    total: int
    per_page: int
    current_page: int
    from_: Optional[int] = Field(alias="from")
    to: Optional[int]
    last_page: int
    has_more_pages: bool


class GetReportsReportDataReportsData(BaseModel):
    code: str
    title: str
    start_time: float = Field(alias="startTime")
    end_time: float = Field(alias="endTime")
    zone: Optional["GetReportsReportDataReportsDataZone"]
    guild: Optional["GetReportsReportDataReportsDataGuild"]
    owner: Optional["GetReportsReportDataReportsDataOwner"]


class GetReportsReportDataReportsDataZone(BaseModel):
    id: int
    name: str


class GetReportsReportDataReportsDataGuild(BaseModel):
    id: int
    name: str
    server: "GetReportsReportDataReportsDataGuildServer"


class GetReportsReportDataReportsDataGuildServer(BaseModel):
    name: str
    slug: str
    region: "GetReportsReportDataReportsDataGuildServerRegion"


class GetReportsReportDataReportsDataGuildServerRegion(BaseModel):
    name: str
    slug: str


class GetReportsReportDataReportsDataOwner(BaseModel):
    id: int
    name: str


GetReports.model_rebuild()
GetReportsReportData.model_rebuild()
GetReportsReportDataReports.model_rebuild()
GetReportsReportDataReportsData.model_rebuild()
GetReportsReportDataReportsDataGuild.model_rebuild()
GetReportsReportDataReportsDataGuildServer.model_rebuild()
