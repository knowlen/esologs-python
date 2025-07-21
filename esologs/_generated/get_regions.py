from typing import List, Optional

from pydantic import Field

from esologs._generated.base_model import BaseModel


class GetRegions(BaseModel):
    world_data: Optional["GetRegionsWorldData"] = Field(alias="worldData")


class GetRegionsWorldData(BaseModel):
    regions: Optional[List[Optional["GetRegionsWorldDataRegions"]]]


class GetRegionsWorldDataRegions(BaseModel):
    id: int
    name: str
    subregions: Optional[List[Optional["GetRegionsWorldDataRegionsSubregions"]]]


class GetRegionsWorldDataRegionsSubregions(BaseModel):
    id: int
    name: str


GetRegions.model_rebuild()
GetRegionsWorldData.model_rebuild()
GetRegionsWorldDataRegions.model_rebuild()
