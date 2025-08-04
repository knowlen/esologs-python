# Analysis: Nested GraphQL Fields Not Exposed in Python Client

## Overview

The ESO Logs Python client provides 100% coverage of the top-level API methods (42/42), but some GraphQL schema fields are only accessible through nested queries that our current implementation doesn't expose.

## Missing Nested Fields

### 1. Encounter.characterRankings
- **Location**: `worldData.zones[].encounters[].characterRankings`
- **Purpose**: Get character rankings for a specific encounter
- **Additional Parameters**:
  - `externalBuffs: ExternalBuffRankFilter` - Filter by external buff usage
  - `hardModeLevel: HardModeLevelRankFilter` - Filter by hard mode level
  - `leaderboard: LeaderboardRank` - Include/exclude ranks without logs
- **Use Case**: More granular ranking queries with additional filtering options

### 2. Encounter.fightRankings
- **Location**: `worldData.zones[].encounters[].fightRankings`
- **Purpose**: Get fight-specific rankings
- **Additional Parameters**:
  - `hardModeLevel: HardModeLevelRankFilter`
  - `leaderboard: LeaderboardRank`

## Current Limitations

1. **No External Buff Filtering**: Users cannot filter rankings based on external buff usage
2. **No Hard Mode Level Filtering**: Cannot filter by specific hard mode levels (0-4)
3. **No Leaderboard Filtering**: Cannot exclude ranks without backing logs

## Potential Solutions

### Option 1: Add Nested Query Support
```python
# Example API addition
async def get_encounter_character_rankings(
    encounter_id: int,
    zone_id: int,
    external_buffs: Optional[ExternalBuffRankFilter] = None,
    hard_mode_level: Optional[HardModeLevelRankFilter] = None,
    leaderboard: Optional[LeaderboardRank] = None,
    # ... other existing parameters
):
    """Get character rankings for a specific encounter with additional filters."""
    pass
```

### Option 2: Provide GraphQL Escape Hatch
```python
# Allow users to execute custom GraphQL queries
async def execute_graphql(
    query: str,
    variables: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Execute a custom GraphQL query for advanced use cases."""
    pass
```

### Option 3: Document the Limitation
- Add a section to docs explaining what's not available
- Show users how to use the underlying GraphQL client directly for advanced queries

## Recommendation

1. **Short term**: Document the limitation and show how to access the GraphQL client directly
2. **Medium term**: Add the most requested nested queries (if users ask for them)
3. **Long term**: Consider a GraphQL escape hatch for power users

## Impact Assessment

- Most users likely don't need these advanced filtering options
- The missing fields are primarily for competitive/ranking analysis
- Current implementation covers all basic use cases
