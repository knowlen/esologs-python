from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel


class GetWorldData(BaseModel):
    world_data: Optional["GetWorldDataWorldData"] = Field(alias="worldData")


class GetWorldDataWorldData(BaseModel):
    encounter: Optional["GetWorldDataWorldDataEncounter"]
    expansion: Optional["GetWorldDataWorldDataExpansion"]
    expansions: Optional[List[Optional["GetWorldDataWorldDataExpansions"]]]
    region: Optional["GetWorldDataWorldDataRegion"]
    regions: Optional[List[Optional["GetWorldDataWorldDataRegions"]]]
    server: Optional["GetWorldDataWorldDataServer"]
    subregion: Optional["GetWorldDataWorldDataSubregion"]
    zone: Optional["GetWorldDataWorldDataZone"]
    zones: Optional[List[Optional["GetWorldDataWorldDataZones"]]]


class GetWorldDataWorldDataEncounter(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataExpansion(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataExpansions(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataRegion(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataRegions(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataServer(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataSubregion(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataZone(BaseModel):
    id: int
    name: str
    frozen: bool
    expansion: "GetWorldDataWorldDataZoneExpansion"
    difficulties: Optional[List[Optional["GetWorldDataWorldDataZoneDifficulties"]]]
    encounters: Optional[List[Optional["GetWorldDataWorldDataZoneEncounters"]]]
    partitions: Optional[List[Optional["GetWorldDataWorldDataZonePartitions"]]]


class GetWorldDataWorldDataZoneExpansion(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataZoneDifficulties(BaseModel):
    id: int
    name: str
    sizes: Optional[List[Optional[int]]]


class GetWorldDataWorldDataZoneEncounters(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataZonePartitions(BaseModel):
    id: int
    name: str
    compact_name: str = Field(alias="compactName")
    default: bool


class GetWorldDataWorldDataZones(BaseModel):
    id: int
    name: str
    frozen: bool
    expansion: "GetWorldDataWorldDataZonesExpansion"
    brackets: Optional["GetWorldDataWorldDataZonesBrackets"]
    difficulties: Optional[List[Optional["GetWorldDataWorldDataZonesDifficulties"]]]
    encounters: Optional[List[Optional["GetWorldDataWorldDataZonesEncounters"]]]
    partitions: Optional[List[Optional["GetWorldDataWorldDataZonesPartitions"]]]


class GetWorldDataWorldDataZonesExpansion(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataZonesBrackets(BaseModel):
    min: float
    max: float
    bucket: float
    type: Optional[str]


class GetWorldDataWorldDataZonesDifficulties(BaseModel):
    id: int
    name: str
    sizes: Optional[List[Optional[int]]]


class GetWorldDataWorldDataZonesEncounters(BaseModel):
    id: int
    name: str


class GetWorldDataWorldDataZonesPartitions(BaseModel):
    id: int
    name: str
    compact_name: str = Field(alias="compactName")
    default: bool


GetWorldData.model_rebuild()
GetWorldDataWorldData.model_rebuild()
GetWorldDataWorldDataZone.model_rebuild()
GetWorldDataWorldDataZones.model_rebuild()
