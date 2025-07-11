from typing import Any, Dict, List, Optional, Union

from .async_base_client import AsyncBaseClient
from .base_model import UNSET, UnsetType
from .enums import (
    CharacterRankingMetricType,
    EventDataType,
    GraphDataType,
    HostilityType,
    KillType,
    RankingCompareType,
    RankingTimeframeType,
    ReportRankingMetricType,
    RoleType,
    TableDataType,
    ViewType,
)
from .get_abilities import GetAbilities
from .get_ability import GetAbility
from .get_character_by_id import GetCharacterById
from .get_character_encounter_ranking import GetCharacterEncounterRanking
from .get_character_encounter_rankings import GetCharacterEncounterRankings
from .get_character_reports import GetCharacterReports
from .get_character_zone_rankings import GetCharacterZoneRankings
from .get_class import GetClass
from .get_classes import GetClasses
from .get_encounters_by_zone import GetEncountersByZone
from .get_factions import GetFactions
from .get_guild_by_id import GetGuildById
from .get_item import GetItem
from .get_item_set import GetItemSet
from .get_item_sets import GetItemSets
from .get_items import GetItems
from .get_map import GetMap
from .get_maps import GetMaps
from .get_npcs import GetNPCs
from .get_npc import GetNPC
from .get_rate_limit_data import GetRateLimitData
from .get_regions import GetRegions
from .get_report_by_code import GetReportByCode
from .get_report_events import GetReportEvents
from .get_report_graph import GetReportGraph
from .get_report_player_details import GetReportPlayerDetails
from .get_report_rankings import GetReportRankings
from .get_report_table import GetReportTable
from .get_reports import GetReports
from .get_world_data import GetWorldData
from .get_zones import GetZones


def gql(q: str) -> str:
    return q


class Client(AsyncBaseClient):
    async def get_ability(self, id: int, **kwargs: Any) -> GetAbility:
        query = gql(
            """
            query getAbility($id: Int!) {
              gameData {
                ability(id: $id) {
                  id
                  name
                  icon
                  description
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getAbility", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAbility.model_validate(data)

    async def get_abilities(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetAbilities:
        query = gql(
            """
            query getAbilities($limit: Int, $page: Int) {
              gameData {
                abilities(limit: $limit, page: $page) {
                  data {
                    id
                    name
                    icon
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"limit": limit, "page": page}
        response = await self.execute(
            query=query, operation_name="getAbilities", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetAbilities.model_validate(data)

    async def get_class(self, id: int, **kwargs: Any) -> GetClass:
        query = gql(
            """
            query getClass($id: Int!) {
              gameData {
                class(id: $id) {
                  id
                  name
                  slug
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getClass", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetClass.model_validate(data)

    async def get_world_data(self, **kwargs: Any) -> GetWorldData:
        query = gql(
            """
            query getWorldData {
              worldData {
                encounter {
                  id
                  name
                }
                expansion {
                  id
                  name
                }
                expansions {
                  id
                  name
                }
                region {
                  id
                  name
                }
                regions {
                  id
                  name
                }
                server {
                  id
                  name
                }
                subregion {
                  id
                  name
                }
                zone {
                  id
                  name
                  frozen
                  expansion {
                    id
                    name
                  }
                  difficulties {
                    id
                    name
                    sizes
                  }
                  encounters {
                    id
                    name
                  }
                  partitions {
                    id
                    name
                    compactName
                    default
                  }
                }
                zones {
                  id
                  name
                  frozen
                  expansion {
                    id
                    name
                  }
                  brackets {
                    min
                    max
                    bucket
                    type
                  }
                  difficulties {
                    id
                    name
                    sizes
                  }
                  encounters {
                    id
                    name
                  }
                  partitions {
                    id
                    name
                    compactName
                    default
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getWorldData", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetWorldData.model_validate(data)

    async def get_character_by_id(self, id: int, **kwargs: Any) -> GetCharacterById:
        query = gql(
            """
            query getCharacterById($id: Int!) {
              characterData {
                character(id: $id) {
                  id
                  name
                  classID
                  raceID
                  guildRank
                  hidden
                  server {
                    name
                    region {
                      name
                    }
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query,
            operation_name="getCharacterById",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCharacterById.model_validate(data)

    async def get_character_reports(
        self,
        character_id: int,
        limit: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetCharacterReports:
        query = gql(
            """
            query getCharacterReports($characterId: Int!, $limit: Int = 10) {
              characterData {
                character(id: $characterId) {
                  recentReports(limit: $limit) {
                    data {
                      code
                      startTime
                      endTime
                      zone {
                        name
                      }
                    }
                    total
                    per_page
                    current_page
                    from
                    to
                    last_page
                    has_more_pages
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"characterId": character_id, "limit": limit}
        response = await self.execute(
            query=query,
            operation_name="getCharacterReports",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCharacterReports.model_validate(data)

    async def get_guild_by_id(self, guild_id: int, **kwargs: Any) -> GetGuildById:
        query = gql(
            """
            query getGuildById($guildId: Int!) {
              guildData {
                guild(id: $guildId) {
                  id
                  name
                  description
                  faction {
                    name
                  }
                  server {
                    name
                    region {
                      name
                    }
                  }
                  tags {
                    id
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"guildId": guild_id}
        response = await self.execute(
            query=query, operation_name="getGuildById", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetGuildById.model_validate(data)

    async def get_encounters_by_zone(
        self, zone_id: int, **kwargs: Any
    ) -> GetEncountersByZone:
        query = gql(
            """
            query getEncountersByZone($zoneId: Int!) {
              worldData {
                zone(id: $zoneId) {
                  id
                  name
                  encounters {
                    id
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"zoneId": zone_id}
        response = await self.execute(
            query=query,
            operation_name="getEncountersByZone",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetEncountersByZone.model_validate(data)

    async def get_regions(self, **kwargs: Any) -> GetRegions:
        query = gql(
            """
            query getRegions {
              worldData {
                regions {
                  id
                  name
                  subregions {
                    id
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getRegions", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetRegions.model_validate(data)

    async def get_report_by_code(self, code: str, **kwargs: Any) -> GetReportByCode:
        query = gql(
            """
            query getReportByCode($code: String!) {
              reportData {
                report(code: $code) {
                  code
                  startTime
                  endTime
                  title
                  visibility
                  zone {
                    name
                  }
                  fights {
                    id
                    name
                    difficulty
                    startTime
                    endTime
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"code": code}
        response = await self.execute(
            query=query, operation_name="getReportByCode", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetReportByCode.model_validate(data)

    async def get_character_encounter_ranking(
        self, character_id: int, encounter_id: int, **kwargs: Any
    ) -> GetCharacterEncounterRanking:
        query = gql(
            """
            query getCharacterEncounterRanking($characterId: Int!, $encounterId: Int!) {
              characterData {
                character(id: $characterId) {
                  encounterRankings(encounterID: $encounterId)
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "characterId": character_id,
            "encounterId": encounter_id,
        }
        response = await self.execute(
            query=query,
            operation_name="getCharacterEncounterRanking",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCharacterEncounterRanking.model_validate(data)

    async def get_character_encounter_rankings(
        self,
        character_id: int,
        encounter_id: int,
        by_bracket: Union[Optional[bool], UnsetType] = UNSET,
        class_name: Union[Optional[str], UnsetType] = UNSET,
        compare: Union[Optional[RankingCompareType], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        include_combatant_info: Union[Optional[bool], UnsetType] = UNSET,
        include_private_logs: Union[Optional[bool], UnsetType] = UNSET,
        metric: Union[Optional[CharacterRankingMetricType], UnsetType] = UNSET,
        partition: Union[Optional[int], UnsetType] = UNSET,
        role: Union[Optional[RoleType], UnsetType] = UNSET,
        size: Union[Optional[int], UnsetType] = UNSET,
        spec_name: Union[Optional[str], UnsetType] = UNSET,
        timeframe: Union[Optional[RankingTimeframeType], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetCharacterEncounterRankings:
        query = gql(
            """
            query getCharacterEncounterRankings($characterId: Int!, $encounterId: Int!, $byBracket: Boolean, $className: String, $compare: RankingCompareType, $difficulty: Int, $includeCombatantInfo: Boolean, $includePrivateLogs: Boolean, $metric: CharacterRankingMetricType, $partition: Int, $role: RoleType, $size: Int, $specName: String, $timeframe: RankingTimeframeType) {
              characterData {
                character(id: $characterId) {
                  encounterRankings(
                    encounterID: $encounterId
                    byBracket: $byBracket
                    className: $className
                    compare: $compare
                    difficulty: $difficulty
                    includeCombatantInfo: $includeCombatantInfo
                    includePrivateLogs: $includePrivateLogs
                    metric: $metric
                    partition: $partition
                    role: $role
                    size: $size
                    specName: $specName
                    timeframe: $timeframe
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "characterId": character_id,
            "encounterId": encounter_id,
            "byBracket": by_bracket,
            "className": class_name,
            "compare": compare,
            "difficulty": difficulty,
            "includeCombatantInfo": include_combatant_info,
            "includePrivateLogs": include_private_logs,
            "metric": metric,
            "partition": partition,
            "role": role,
            "size": size,
            "specName": spec_name,
            "timeframe": timeframe,
        }
        response = await self.execute(
            query=query,
            operation_name="getCharacterEncounterRankings",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCharacterEncounterRankings.model_validate(data)

    async def get_character_zone_rankings(
        self,
        character_id: int,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        by_bracket: Union[Optional[bool], UnsetType] = UNSET,
        class_name: Union[Optional[str], UnsetType] = UNSET,
        compare: Union[Optional[RankingCompareType], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        include_private_logs: Union[Optional[bool], UnsetType] = UNSET,
        metric: Union[Optional[CharacterRankingMetricType], UnsetType] = UNSET,
        partition: Union[Optional[int], UnsetType] = UNSET,
        role: Union[Optional[RoleType], UnsetType] = UNSET,
        size: Union[Optional[int], UnsetType] = UNSET,
        spec_name: Union[Optional[str], UnsetType] = UNSET,
        timeframe: Union[Optional[RankingTimeframeType], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetCharacterZoneRankings:
        query = gql(
            """
            query getCharacterZoneRankings($characterId: Int!, $zoneId: Int, $byBracket: Boolean, $className: String, $compare: RankingCompareType, $difficulty: Int, $includePrivateLogs: Boolean, $metric: CharacterRankingMetricType, $partition: Int, $role: RoleType, $size: Int, $specName: String, $timeframe: RankingTimeframeType) {
              characterData {
                character(id: $characterId) {
                  zoneRankings(
                    zoneID: $zoneId
                    byBracket: $byBracket
                    className: $className
                    compare: $compare
                    difficulty: $difficulty
                    includePrivateLogs: $includePrivateLogs
                    metric: $metric
                    partition: $partition
                    role: $role
                    size: $size
                    specName: $specName
                    timeframe: $timeframe
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "characterId": character_id,
            "zoneId": zone_id,
            "byBracket": by_bracket,
            "className": class_name,
            "compare": compare,
            "difficulty": difficulty,
            "includePrivateLogs": include_private_logs,
            "metric": metric,
            "partition": partition,
            "role": role,
            "size": size,
            "specName": spec_name,
            "timeframe": timeframe,
        }
        response = await self.execute(
            query=query,
            operation_name="getCharacterZoneRankings",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetCharacterZoneRankings.model_validate(data)

    async def get_zones(self, **kwargs: Any) -> GetZones:
        query = gql(
            """
            query getZones {
              worldData {
                zones {
                  id
                  name
                  frozen
                  brackets {
                    type
                    min
                    max
                    bucket
                  }
                  encounters {
                    id
                    name
                  }
                  difficulties {
                    id
                    name
                    sizes
                  }
                  expansion {
                    id
                    name
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getZones", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetZones.model_validate(data)

    async def get_classes(
        self,
        faction_id: Union[Optional[int], UnsetType] = UNSET,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetClasses:
        query = gql(
            """
            query getClasses($faction_id: Int, $zone_id: Int) {
              gameData {
                classes(faction_id: $faction_id, zone_id: $zone_id) {
                  id
                  name
                  slug
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"faction_id": faction_id, "zone_id": zone_id}
        response = await self.execute(
            query=query, operation_name="getClasses", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetClasses.model_validate(data)

    async def get_factions(self, **kwargs: Any) -> GetFactions:
        query = gql(
            """
            query getFactions {
              gameData {
                factions {
                  id
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query, operation_name="getFactions", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetFactions.model_validate(data)

    async def get_item(self, id: int, **kwargs: Any) -> GetItem:
        query = gql(
            """
            query getItem($id: Int!) {
              gameData {
                item(id: $id) {
                  id
                  name
                  icon
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getItem", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetItem.model_validate(data)

    async def get_item_set(self, id: int, **kwargs: Any) -> GetItemSet:
        query = gql(
            """
            query getItemSet($id: Int!) {
              gameData {
                item_set(id: $id) {
                  id
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getItemSet", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetItemSet.model_validate(data)

    async def get_item_sets(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetItemSets:
        query = gql(
            """
            query getItemSets($limit: Int, $page: Int) {
              gameData {
                item_sets(limit: $limit, page: $page) {
                  data {
                    id
                    name
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"limit": limit, "page": page}
        response = await self.execute(
            query=query, operation_name="getItemSets", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetItemSets.model_validate(data)

    async def get_items(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetItems:
        query = gql(
            """
            query getItems($limit: Int, $page: Int) {
              gameData {
                items(limit: $limit, page: $page) {
                  data {
                    id
                    name
                    icon
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"limit": limit, "page": page}
        response = await self.execute(
            query=query, operation_name="getItems", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetItems.model_validate(data)

    async def get_map(self, id: int, **kwargs: Any) -> GetMap:
        query = gql(
            """
            query getMap($id: Int!) {
              gameData {
                map(id: $id) {
                  id
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getMap", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetMap.model_validate(data)

    async def get_maps(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetMaps:
        query = gql(
            """
            query getMaps($limit: Int, $page: Int) {
              gameData {
                maps(limit: $limit, page: $page) {
                  data {
                    id
                    name
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"limit": limit, "page": page}
        response = await self.execute(
            query=query, operation_name="getMaps", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetMaps.model_validate(data)

    async def get_npc(self, id: int, **kwargs: Any) -> GetNPC:
        query = gql(
            """
            query getNPC($id: Int!) {
              gameData {
                npc(id: $id) {
                  id
                  name
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"id": id}
        response = await self.execute(
            query=query, operation_name="getNPC", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetNPC.model_validate(data)

    async def get_npcs(
        self,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetNPCs:
        query = gql(
            """
            query getNPCs($limit: Int, $page: Int) {
              gameData {
                npcs(limit: $limit, page: $page) {
                  data {
                    id
                    name
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {"limit": limit, "page": page}
        response = await self.execute(
            query=query, operation_name="getNPCs", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetNPCs.model_validate(data)

    async def get_rate_limit_data(self, **kwargs: Any) -> GetRateLimitData:
        query = gql(
            """
            query getRateLimitData {
              rateLimitData {
                limitPerHour
                pointsSpentThisHour
                pointsResetIn
              }
            }
            """
        )
        variables: Dict[str, object] = {}
        response = await self.execute(
            query=query,
            operation_name="getRateLimitData",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetRateLimitData.model_validate(data)

    async def get_report_events(
        self,
        code: str,
        ability_id: Union[Optional[float], UnsetType] = UNSET,
        data_type: Union[Optional[EventDataType], UnsetType] = UNSET,
        death: Union[Optional[int], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        encounter_id: Union[Optional[int], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        fight_i_ds: Union[Optional[List[Optional[int]]], UnsetType] = UNSET,
        filter_expression: Union[Optional[str], UnsetType] = UNSET,
        hostility_type: Union[Optional[HostilityType], UnsetType] = UNSET,
        include_resources: Union[Optional[bool], UnsetType] = UNSET,
        kill_type: Union[Optional[KillType], UnsetType] = UNSET,
        limit: Union[Optional[int], UnsetType] = UNSET,
        source_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        source_auras_present: Union[Optional[str], UnsetType] = UNSET,
        source_class: Union[Optional[str], UnsetType] = UNSET,
        source_id: Union[Optional[int], UnsetType] = UNSET,
        source_instance_id: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        target_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        target_auras_present: Union[Optional[str], UnsetType] = UNSET,
        target_class: Union[Optional[str], UnsetType] = UNSET,
        target_id: Union[Optional[int], UnsetType] = UNSET,
        target_instance_id: Union[Optional[int], UnsetType] = UNSET,
        translate: Union[Optional[bool], UnsetType] = UNSET,
        use_ability_i_ds: Union[Optional[bool], UnsetType] = UNSET,
        use_actor_i_ds: Union[Optional[bool], UnsetType] = UNSET,
        view_options: Union[Optional[int], UnsetType] = UNSET,
        wipe_cutoff: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReportEvents:
        query = gql(
            """
            query getReportEvents($code: String!, $abilityID: Float, $dataType: EventDataType, $death: Int, $difficulty: Int, $encounterID: Int, $endTime: Float, $fightIDs: [Int], $filterExpression: String, $hostilityType: HostilityType, $includeResources: Boolean, $killType: KillType, $limit: Int, $sourceAurasAbsent: String, $sourceAurasPresent: String, $sourceClass: String, $sourceID: Int, $sourceInstanceID: Int, $startTime: Float, $targetAurasAbsent: String, $targetAurasPresent: String, $targetClass: String, $targetID: Int, $targetInstanceID: Int, $translate: Boolean, $useAbilityIDs: Boolean, $useActorIDs: Boolean, $viewOptions: Int, $wipeCutoff: Int) {
              reportData {
                report(code: $code) {
                  events(
                    abilityID: $abilityID
                    dataType: $dataType
                    death: $death
                    difficulty: $difficulty
                    encounterID: $encounterID
                    endTime: $endTime
                    fightIDs: $fightIDs
                    filterExpression: $filterExpression
                    hostilityType: $hostilityType
                    includeResources: $includeResources
                    killType: $killType
                    limit: $limit
                    sourceAurasAbsent: $sourceAurasAbsent
                    sourceAurasPresent: $sourceAurasPresent
                    sourceClass: $sourceClass
                    sourceID: $sourceID
                    sourceInstanceID: $sourceInstanceID
                    startTime: $startTime
                    targetAurasAbsent: $targetAurasAbsent
                    targetAurasPresent: $targetAurasPresent
                    targetClass: $targetClass
                    targetID: $targetID
                    targetInstanceID: $targetInstanceID
                    translate: $translate
                    useAbilityIDs: $useAbilityIDs
                    useActorIDs: $useActorIDs
                    viewOptions: $viewOptions
                    wipeCutoff: $wipeCutoff
                  ) {
                    data
                    nextPageTimestamp
                  }
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "code": code,
            "abilityID": ability_id,
            "dataType": data_type,
            "death": death,
            "difficulty": difficulty,
            "encounterID": encounter_id,
            "endTime": end_time,
            "fightIDs": fight_i_ds,
            "filterExpression": filter_expression,
            "hostilityType": hostility_type,
            "includeResources": include_resources,
            "killType": kill_type,
            "limit": limit,
            "sourceAurasAbsent": source_auras_absent,
            "sourceAurasPresent": source_auras_present,
            "sourceClass": source_class,
            "sourceID": source_id,
            "sourceInstanceID": source_instance_id,
            "startTime": start_time,
            "targetAurasAbsent": target_auras_absent,
            "targetAurasPresent": target_auras_present,
            "targetClass": target_class,
            "targetID": target_id,
            "targetInstanceID": target_instance_id,
            "translate": translate,
            "useAbilityIDs": use_ability_i_ds,
            "useActorIDs": use_actor_i_ds,
            "viewOptions": view_options,
            "wipeCutoff": wipe_cutoff,
        }
        response = await self.execute(
            query=query, operation_name="getReportEvents", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetReportEvents.model_validate(data)

    async def get_report_graph(
        self,
        code: str,
        ability_id: Union[Optional[float], UnsetType] = UNSET,
        data_type: Union[Optional[GraphDataType], UnsetType] = UNSET,
        death: Union[Optional[int], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        encounter_id: Union[Optional[int], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        fight_i_ds: Union[Optional[List[Optional[int]]], UnsetType] = UNSET,
        filter_expression: Union[Optional[str], UnsetType] = UNSET,
        hostility_type: Union[Optional[HostilityType], UnsetType] = UNSET,
        kill_type: Union[Optional[KillType], UnsetType] = UNSET,
        source_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        source_auras_present: Union[Optional[str], UnsetType] = UNSET,
        source_class: Union[Optional[str], UnsetType] = UNSET,
        source_id: Union[Optional[int], UnsetType] = UNSET,
        source_instance_id: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        target_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        target_auras_present: Union[Optional[str], UnsetType] = UNSET,
        target_class: Union[Optional[str], UnsetType] = UNSET,
        target_id: Union[Optional[int], UnsetType] = UNSET,
        target_instance_id: Union[Optional[int], UnsetType] = UNSET,
        translate: Union[Optional[bool], UnsetType] = UNSET,
        view_options: Union[Optional[int], UnsetType] = UNSET,
        view_by: Union[Optional[ViewType], UnsetType] = UNSET,
        wipe_cutoff: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReportGraph:
        query = gql(
            """
            query getReportGraph($code: String!, $abilityID: Float, $dataType: GraphDataType, $death: Int, $difficulty: Int, $encounterID: Int, $endTime: Float, $fightIDs: [Int], $filterExpression: String, $hostilityType: HostilityType, $killType: KillType, $sourceAurasAbsent: String, $sourceAurasPresent: String, $sourceClass: String, $sourceID: Int, $sourceInstanceID: Int, $startTime: Float, $targetAurasAbsent: String, $targetAurasPresent: String, $targetClass: String, $targetID: Int, $targetInstanceID: Int, $translate: Boolean, $viewOptions: Int, $viewBy: ViewType, $wipeCutoff: Int) {
              reportData {
                report(code: $code) {
                  graph(
                    abilityID: $abilityID
                    dataType: $dataType
                    death: $death
                    difficulty: $difficulty
                    encounterID: $encounterID
                    endTime: $endTime
                    fightIDs: $fightIDs
                    filterExpression: $filterExpression
                    hostilityType: $hostilityType
                    killType: $killType
                    sourceAurasAbsent: $sourceAurasAbsent
                    sourceAurasPresent: $sourceAurasPresent
                    sourceClass: $sourceClass
                    sourceID: $sourceID
                    sourceInstanceID: $sourceInstanceID
                    startTime: $startTime
                    targetAurasAbsent: $targetAurasAbsent
                    targetAurasPresent: $targetAurasPresent
                    targetClass: $targetClass
                    targetID: $targetID
                    targetInstanceID: $targetInstanceID
                    translate: $translate
                    viewOptions: $viewOptions
                    viewBy: $viewBy
                    wipeCutoff: $wipeCutoff
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "code": code,
            "abilityID": ability_id,
            "dataType": data_type,
            "death": death,
            "difficulty": difficulty,
            "encounterID": encounter_id,
            "endTime": end_time,
            "fightIDs": fight_i_ds,
            "filterExpression": filter_expression,
            "hostilityType": hostility_type,
            "killType": kill_type,
            "sourceAurasAbsent": source_auras_absent,
            "sourceAurasPresent": source_auras_present,
            "sourceClass": source_class,
            "sourceID": source_id,
            "sourceInstanceID": source_instance_id,
            "startTime": start_time,
            "targetAurasAbsent": target_auras_absent,
            "targetAurasPresent": target_auras_present,
            "targetClass": target_class,
            "targetID": target_id,
            "targetInstanceID": target_instance_id,
            "translate": translate,
            "viewOptions": view_options,
            "viewBy": view_by,
            "wipeCutoff": wipe_cutoff,
        }
        response = await self.execute(
            query=query, operation_name="getReportGraph", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetReportGraph.model_validate(data)

    async def get_report_table(
        self,
        code: str,
        ability_id: Union[Optional[float], UnsetType] = UNSET,
        data_type: Union[Optional[TableDataType], UnsetType] = UNSET,
        death: Union[Optional[int], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        encounter_id: Union[Optional[int], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        fight_i_ds: Union[Optional[List[Optional[int]]], UnsetType] = UNSET,
        filter_expression: Union[Optional[str], UnsetType] = UNSET,
        hostility_type: Union[Optional[HostilityType], UnsetType] = UNSET,
        kill_type: Union[Optional[KillType], UnsetType] = UNSET,
        source_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        source_auras_present: Union[Optional[str], UnsetType] = UNSET,
        source_class: Union[Optional[str], UnsetType] = UNSET,
        source_id: Union[Optional[int], UnsetType] = UNSET,
        source_instance_id: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        target_auras_absent: Union[Optional[str], UnsetType] = UNSET,
        target_auras_present: Union[Optional[str], UnsetType] = UNSET,
        target_class: Union[Optional[str], UnsetType] = UNSET,
        target_id: Union[Optional[int], UnsetType] = UNSET,
        target_instance_id: Union[Optional[int], UnsetType] = UNSET,
        translate: Union[Optional[bool], UnsetType] = UNSET,
        view_options: Union[Optional[int], UnsetType] = UNSET,
        view_by: Union[Optional[ViewType], UnsetType] = UNSET,
        wipe_cutoff: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReportTable:
        query = gql(
            """
            query getReportTable($code: String!, $abilityID: Float, $dataType: TableDataType, $death: Int, $difficulty: Int, $encounterID: Int, $endTime: Float, $fightIDs: [Int], $filterExpression: String, $hostilityType: HostilityType, $killType: KillType, $sourceAurasAbsent: String, $sourceAurasPresent: String, $sourceClass: String, $sourceID: Int, $sourceInstanceID: Int, $startTime: Float, $targetAurasAbsent: String, $targetAurasPresent: String, $targetClass: String, $targetID: Int, $targetInstanceID: Int, $translate: Boolean, $viewOptions: Int, $viewBy: ViewType, $wipeCutoff: Int) {
              reportData {
                report(code: $code) {
                  table(
                    abilityID: $abilityID
                    dataType: $dataType
                    death: $death
                    difficulty: $difficulty
                    encounterID: $encounterID
                    endTime: $endTime
                    fightIDs: $fightIDs
                    filterExpression: $filterExpression
                    hostilityType: $hostilityType
                    killType: $killType
                    sourceAurasAbsent: $sourceAurasAbsent
                    sourceAurasPresent: $sourceAurasPresent
                    sourceClass: $sourceClass
                    sourceID: $sourceID
                    sourceInstanceID: $sourceInstanceID
                    startTime: $startTime
                    targetAurasAbsent: $targetAurasAbsent
                    targetAurasPresent: $targetAurasPresent
                    targetClass: $targetClass
                    targetID: $targetID
                    targetInstanceID: $targetInstanceID
                    translate: $translate
                    viewOptions: $viewOptions
                    viewBy: $viewBy
                    wipeCutoff: $wipeCutoff
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "code": code,
            "abilityID": ability_id,
            "dataType": data_type,
            "death": death,
            "difficulty": difficulty,
            "encounterID": encounter_id,
            "endTime": end_time,
            "fightIDs": fight_i_ds,
            "filterExpression": filter_expression,
            "hostilityType": hostility_type,
            "killType": kill_type,
            "sourceAurasAbsent": source_auras_absent,
            "sourceAurasPresent": source_auras_present,
            "sourceClass": source_class,
            "sourceID": source_id,
            "sourceInstanceID": source_instance_id,
            "startTime": start_time,
            "targetAurasAbsent": target_auras_absent,
            "targetAurasPresent": target_auras_present,
            "targetClass": target_class,
            "targetID": target_id,
            "targetInstanceID": target_instance_id,
            "translate": translate,
            "viewOptions": view_options,
            "viewBy": view_by,
            "wipeCutoff": wipe_cutoff,
        }
        response = await self.execute(
            query=query, operation_name="getReportTable", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetReportTable.model_validate(data)

    async def get_report_rankings(
        self,
        code: str,
        compare: Union[Optional[RankingCompareType], UnsetType] = UNSET,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        encounter_id: Union[Optional[int], UnsetType] = UNSET,
        fight_i_ds: Union[Optional[List[Optional[int]]], UnsetType] = UNSET,
        player_metric: Union[Optional[ReportRankingMetricType], UnsetType] = UNSET,
        timeframe: Union[Optional[RankingTimeframeType], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReportRankings:
        query = gql(
            """
            query getReportRankings($code: String!, $compare: RankingCompareType, $difficulty: Int, $encounterID: Int, $fightIDs: [Int], $playerMetric: ReportRankingMetricType, $timeframe: RankingTimeframeType) {
              reportData {
                report(code: $code) {
                  rankings(
                    compare: $compare
                    difficulty: $difficulty
                    encounterID: $encounterID
                    fightIDs: $fightIDs
                    playerMetric: $playerMetric
                    timeframe: $timeframe
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "code": code,
            "compare": compare,
            "difficulty": difficulty,
            "encounterID": encounter_id,
            "fightIDs": fight_i_ds,
            "playerMetric": player_metric,
            "timeframe": timeframe,
        }
        response = await self.execute(
            query=query,
            operation_name="getReportRankings",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetReportRankings.model_validate(data)

    async def get_report_player_details(
        self,
        code: str,
        difficulty: Union[Optional[int], UnsetType] = UNSET,
        encounter_id: Union[Optional[int], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        fight_i_ds: Union[Optional[List[Optional[int]]], UnsetType] = UNSET,
        kill_type: Union[Optional[KillType], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        translate: Union[Optional[bool], UnsetType] = UNSET,
        include_combatant_info: Union[Optional[bool], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReportPlayerDetails:
        query = gql(
            """
            query getReportPlayerDetails($code: String!, $difficulty: Int, $encounterID: Int, $endTime: Float, $fightIDs: [Int], $killType: KillType, $startTime: Float, $translate: Boolean, $includeCombatantInfo: Boolean) {
              reportData {
                report(code: $code) {
                  playerDetails(
                    difficulty: $difficulty
                    encounterID: $encounterID
                    endTime: $endTime
                    fightIDs: $fightIDs
                    killType: $killType
                    startTime: $startTime
                    translate: $translate
                    includeCombatantInfo: $includeCombatantInfo
                  )
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "code": code,
            "difficulty": difficulty,
            "encounterID": encounter_id,
            "endTime": end_time,
            "fightIDs": fight_i_ds,
            "killType": kill_type,
            "startTime": start_time,
            "translate": translate,
            "includeCombatantInfo": include_combatant_info,
        }
        response = await self.execute(
            query=query,
            operation_name="getReportPlayerDetails",
            variables=variables,
            **kwargs
        )
        data = self.get_data(response)
        return GetReportPlayerDetails.model_validate(data)

    async def get_reports(
        self,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        guild_id: Union[Optional[int], UnsetType] = UNSET,
        guild_name: Union[Optional[str], UnsetType] = UNSET,
        guild_server_slug: Union[Optional[str], UnsetType] = UNSET,
        guild_server_region: Union[Optional[str], UnsetType] = UNSET,
        guild_tag_id: Union[Optional[int], UnsetType] = UNSET,
        user_id: Union[Optional[int], UnsetType] = UNSET,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        game_zone_id: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any
    ) -> GetReports:
        query = gql(
            """
            query getReports($endTime: Float, $guildID: Int, $guildName: String, $guildServerSlug: String, $guildServerRegion: String, $guildTagID: Int, $userID: Int, $limit: Int, $page: Int, $startTime: Float, $zoneID: Int, $gameZoneID: Int) {
              reportData {
                reports(
                  endTime: $endTime
                  guildID: $guildID
                  guildName: $guildName
                  guildServerSlug: $guildServerSlug
                  guildServerRegion: $guildServerRegion
                  guildTagID: $guildTagID
                  userID: $userID
                  limit: $limit
                  page: $page
                  startTime: $startTime
                  zoneID: $zoneID
                  gameZoneID: $gameZoneID
                ) {
                  data {
                    code
                    title
                    startTime
                    endTime
                    zone {
                      id
                      name
                    }
                    guild {
                      id
                      name
                      server {
                        name
                        slug
                        region {
                          name
                          slug
                        }
                      }
                    }
                    owner {
                      id
                      name
                    }
                  }
                  total
                  per_page
                  current_page
                  from
                  to
                  last_page
                  has_more_pages
                }
              }
            }
            """
        )
        variables: Dict[str, object] = {
            "endTime": end_time,
            "guildID": guild_id,
            "guildName": guild_name,
            "guildServerSlug": guild_server_slug,
            "guildServerRegion": guild_server_region,
            "guildTagID": guild_tag_id,
            "userID": user_id,
            "limit": limit,
            "page": page,
            "startTime": start_time,
            "zoneID": zone_id,
            "gameZoneID": game_zone_id,
        }
        response = await self.execute(
            query=query, operation_name="getReports", variables=variables, **kwargs
        )
        data = self.get_data(response)
        return GetReports.model_validate(data)

    async def search_reports(
        self,
        guild_id: Union[Optional[int], UnsetType] = UNSET,
        guild_name: Union[Optional[str], UnsetType] = UNSET,
        guild_server_slug: Union[Optional[str], UnsetType] = UNSET,
        guild_server_region: Union[Optional[str], UnsetType] = UNSET,
        guild_tag_id: Union[Optional[int], UnsetType] = UNSET,
        user_id: Union[Optional[int], UnsetType] = UNSET,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        game_zone_id: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetReports:
        """
        Search for reports with flexible filtering options.
        
        Args:
            guild_id: Filter by specific guild ID
            guild_name: Filter by guild name (requires guild_server_slug and guild_server_region)
            guild_server_slug: Guild server slug (required with guild_name)
            guild_server_region: Guild server region (required with guild_name)
            guild_tag_id: Filter by guild tag/team ID
            user_id: Filter by specific user ID
            zone_id: Filter by zone ID
            game_zone_id: Filter by game zone ID
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)
            
        Returns:
            GetReports: Paginated list of reports matching the criteria
            
        Examples:
            # Search by guild ID
            reports = await client.search_reports(guild_id=123)
            
            # Search by guild name
            reports = await client.search_reports(
                guild_name="My Guild", 
                guild_server_slug="server-name",
                guild_server_region="NA"
            )
            
            # Search with date range
            reports = await client.search_reports(
                user_id=456,
                start_time=1640995200000,  # Jan 1, 2022
                end_time=1672531200000     # Jan 1, 2023
            )
        """
        return await self.get_reports(
            end_time=end_time,
            guild_id=guild_id,
            guild_name=guild_name,
            guild_server_slug=guild_server_slug,
            guild_server_region=guild_server_region,
            guild_tag_id=guild_tag_id,
            user_id=user_id,
            limit=limit,
            page=page,
            start_time=start_time,
            zone_id=zone_id,
            game_zone_id=game_zone_id,
            **kwargs,
        )

    async def get_guild_reports(
        self,
        guild_id: int,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetReports:
        """
        Convenience method to get reports for a specific guild.
        
        Args:
            guild_id: The guild ID to search for
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            zone_id: Filter by specific zone
            
        Returns:
            GetReports: Paginated list of guild reports
            
        Example:
            # Get recent reports for guild
            reports = await client.get_guild_reports(guild_id=123, limit=25)
        """
        return await self.search_reports(
            guild_id=guild_id,
            limit=limit,
            page=page,
            start_time=start_time,
            end_time=end_time,
            zone_id=zone_id,
            **kwargs,
        )

    async def get_user_reports(
        self,
        user_id: int,
        limit: Union[Optional[int], UnsetType] = UNSET,
        page: Union[Optional[int], UnsetType] = UNSET,
        start_time: Union[Optional[float], UnsetType] = UNSET,
        end_time: Union[Optional[float], UnsetType] = UNSET,
        zone_id: Union[Optional[int], UnsetType] = UNSET,
        **kwargs: Any,
    ) -> GetReports:
        """
        Convenience method to get reports for a specific user.
        
        Args:
            user_id: The user ID to search for
            limit: Number of reports per page (1-25, default 16)
            page: Page number (default 1)
            start_time: Start time filter (UNIX timestamp with milliseconds)
            end_time: End time filter (UNIX timestamp with milliseconds)
            zone_id: Filter by specific zone
            
        Returns:
            GetReports: Paginated list of user reports
            
        Example:
            # Get recent reports for user
            reports = await client.get_user_reports(user_id=456, limit=25)
        """
        return await self.search_reports(
            user_id=user_id,
            limit=limit,
            page=page,
            start_time=start_time,
            end_time=end_time,
            zone_id=zone_id,
            **kwargs,
        )
