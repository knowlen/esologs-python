"""
GraphQL queries for ESO Logs API.

This module contains all GraphQL query strings used by the client.
Queries are organized by their functional area for easy maintenance.
"""

# Game Data Queries
GET_ABILITY = """
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

GET_ABILITIES = """
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

GET_CLASS = """
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

GET_CLASSES = """
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

GET_FACTIONS = """
query getFactions {
  gameData {
    factions {
      id
      name
    }
  }
}
"""

GET_ITEM = """
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

GET_ITEMS = """
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

GET_ITEM_SET = """
query getItemSet($id: Int!) {
  gameData {
    item_set(id: $id) {
      id
      name
    }
  }
}
"""

GET_ITEM_SETS = """
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

GET_MAP = """
query getMap($id: Int!) {
  gameData {
    map(id: $id) {
      id
      name
    }
  }
}
"""

GET_MAPS = """
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

GET_NPC = """
query getNPC($id: Int!) {
  gameData {
    npc(id: $id) {
      id
      name
    }
  }
}
"""

GET_NPCS = """
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

# World Data Queries
GET_WORLD_DATA = """
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

GET_ZONES = """
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

GET_ENCOUNTERS_BY_ZONE = """
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

GET_REGIONS = """
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

# Character Queries
GET_CHARACTER_BY_ID = """
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

GET_CHARACTER_REPORTS = """
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

GET_CHARACTER_ENCOUNTER_RANKING = """
query getCharacterEncounterRanking($characterId: Int!, $encounterId: Int!) {
  characterData {
    character(id: $characterId) {
      encounterRankings(encounterID: $encounterId)
    }
  }
}
"""

GET_CHARACTER_ENCOUNTER_RANKINGS = """
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

GET_CHARACTER_ZONE_RANKINGS = """
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

# Guild Queries
GET_GUILD_BY_ID = """
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

GET_GUILDS = """
query getGuilds($limit: Int, $page: Int, $serverID: Int, $serverSlug: String, $serverRegion: String) {
  guildData {
    guilds(limit: $limit, page: $page, serverID: $serverID, serverSlug: $serverSlug, serverRegion: $serverRegion) {
      total
      per_page
      current_page
      from
      to
      last_page
      has_more_pages
      data {
        id
        name
        faction {
          name
        }
        server {
          name
          region {
            name
          }
        }
      }
    }
  }
}
"""

GET_GUILD_BY_NAME = """
query getGuildByName($name: String!, $serverSlug: String!, $serverRegion: String!) {
  guildData {
    guild(name: $name, serverSlug: $serverSlug, serverRegion: $serverRegion) {
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

GET_GUILD_ATTENDANCE = """
query getGuildAttendance($guildId: Int!, $guildTagID: Int, $limit: Int, $page: Int, $zoneID: Int) {
  guildData {
    guild(id: $guildId) {
      attendance(guildTagID: $guildTagID, limit: $limit, page: $page, zoneID: $zoneID) {
        total
        per_page
        current_page
        has_more_pages
        data {
          code
          startTime
          players {
            name
            type
            presence
          }
        }
      }
    }
  }
}
"""

GET_GUILD_MEMBERS = """
query getGuildMembers($guildId: Int!, $limit: Int, $page: Int) {
  guildData {
    guild(id: $guildId) {
      members(limit: $limit, page: $page) {
        total
        per_page
        current_page
        has_more_pages
        data {
          id
          name
          server {
            name
            region {
              name
            }
          }
          guildRank
        }
      }
    }
  }
}
"""

# Report Queries
GET_REPORT_BY_CODE = """
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

GET_REPORTS = """
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

GET_REPORT_EVENTS = """
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

GET_REPORT_GRAPH = """
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

GET_REPORT_TABLE = """
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

GET_REPORT_RANKINGS = """
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

GET_REPORT_PLAYER_DETAILS = """
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

# Rate Limit Query
GET_RATE_LIMIT_DATA = """
query getRateLimitData {
  rateLimitData {
    limitPerHour
    pointsSpentThisHour
    pointsResetIn
  }
}
"""

# Query mapping for easy access
QUERIES = {
    # Game Data
    "getAbility": GET_ABILITY,
    "getAbilities": GET_ABILITIES,
    "getClass": GET_CLASS,
    "getClasses": GET_CLASSES,
    "getFactions": GET_FACTIONS,
    "getItem": GET_ITEM,
    "getItems": GET_ITEMS,
    "getItemSet": GET_ITEM_SET,
    "getItemSets": GET_ITEM_SETS,
    "getMap": GET_MAP,
    "getMaps": GET_MAPS,
    "getNPC": GET_NPC,
    "getNPCs": GET_NPCS,
    # World Data
    "getWorldData": GET_WORLD_DATA,
    "getZones": GET_ZONES,
    "getEncountersByZone": GET_ENCOUNTERS_BY_ZONE,
    "getRegions": GET_REGIONS,
    # Character
    "getCharacterById": GET_CHARACTER_BY_ID,
    "getCharacterReports": GET_CHARACTER_REPORTS,
    "getCharacterEncounterRanking": GET_CHARACTER_ENCOUNTER_RANKING,
    "getCharacterEncounterRankings": GET_CHARACTER_ENCOUNTER_RANKINGS,
    "getCharacterZoneRankings": GET_CHARACTER_ZONE_RANKINGS,
    # Guild
    "getGuildById": GET_GUILD_BY_ID,
    "getGuilds": GET_GUILDS,
    "getGuildByName": GET_GUILD_BY_NAME,
    "getGuildAttendance": GET_GUILD_ATTENDANCE,
    "getGuildMembers": GET_GUILD_MEMBERS,
    # Reports
    "getReportByCode": GET_REPORT_BY_CODE,
    "getReports": GET_REPORTS,
    "getReportEvents": GET_REPORT_EVENTS,
    "getReportGraph": GET_REPORT_GRAPH,
    "getReportTable": GET_REPORT_TABLE,
    "getReportRankings": GET_REPORT_RANKINGS,
    "getReportPlayerDetails": GET_REPORT_PLAYER_DETAILS,
    # Rate Limit
    "getRateLimitData": GET_RATE_LIMIT_DATA,
}
