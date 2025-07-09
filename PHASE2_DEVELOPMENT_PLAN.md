# 📋 Phase 2 Development Plan: Core Architecture & API Expansion

## 🎯 **Phase 2 Overview**

**Goal**: Transform the current basic GraphQL client into a comprehensive, well-architected library with significantly expanded API coverage.

**Current State**: ~35% API coverage, expanding functionality  
**Target State**: ~60-70% API coverage, production-ready architecture

## 📊 **Current API Coverage Analysis**

### ✅ **What's Currently Implemented (~35%)**
- Basic game data (abilities, classes, items, NPCs, maps, factions)
- Simple character info and reports
- **Character rankings & performance** (get_character_encounter_rankings, get_character_zone_rankings)
- Basic guild information  
- World data (regions, zones, encounters)
- Rate limiting information
- Single report retrieval
- **Comprehensive report analysis** (get_report_events, get_report_graph, get_report_table, get_report_rankings, get_report_player_details)

### ❌ **Major Missing Functionality (~65%)**
Based on schema analysis, we're missing:

#### **High Priority Missing (Critical for users)**
1. ✅ **Character Rankings & Performance** (COMPLETED)
   - ✅ `Character.encounterRankings()` - Character performance for specific encounters
   - ✅ `Character.zoneRankings()` - Zone-wide character leaderboards
   - ✅ Detailed performance metrics (DPS, HPS, etc.)

2. ✅ **Detailed Report Analysis** (COMPLETED)
   - ✅ `Report.events()` - Event-by-event combat log data
   - ✅ `Report.graph()` - Damage/healing graphs and charts
   - ✅ `Report.table()` - Tabular analysis data
   - ✅ `Report.rankings()` - Report performance rankings

3. **Advanced Report Search**
   - `ReportData.reports()` - Search reports by guild, user, dates, zones
   - Comprehensive filtering and pagination

#### **Medium Priority Missing (Important features)**
4. **User Account Integration**
   - `UserData.user()` - User profile information
   - `User.characters` - User's claimed characters
   - `User.guilds` - User's guild memberships

5. **Progress Race Tracking**
   - `ProgressRaceData.progressRace()` - World/realm first tracking
   - Live competition data

6. **Enhanced Guild Features**
   - `Guild.attendance()` - Member attendance tracking
   - `Guild.members()` - Complete guild roster
   - `Guild.zoneRanking()` - Guild performance rankings

## 🏗️ **Proposed Architecture Improvements**

### **1. Client Architecture Redesign**

**Current Issue**: Single monolithic client class with 20+ methods  
**Proposed Solution**: Modular client hierarchy

```python
# New architecture
class EsoLogsClient:
    def __init__(self, token: str):
        self.game_data = GameDataClient(self._base_client)
        self.character_data = CharacterDataClient(self._base_client) 
        self.report_data = ReportDataClient(self._base_client)
        self.rankings = RankingsClient(self._base_client)
        self.world_data = WorldDataClient(self._base_client)
        self.user_data = UserDataClient(self._base_client)
        self.guild_data = GuildDataClient(self._base_client)

# Usage becomes more intuitive
client = EsoLogsClient(token)
character_rankings = await client.rankings.get_character_encounter_rankings(char_id, encounter_id)
reports = await client.report_data.search_reports(guild_id=123, start_date="2025-01-01")
```

### **2. Data Transformation Layer**

**Current Issue**: Raw GraphQL responses, no data transformation  
**Proposed Solution**: Built-in transformation utilities

```python
class DataTransformer:
    def to_dataframe(self, data) -> pd.DataFrame
    def to_dict(self, data) -> dict
    def to_json(self, data) -> str
    def export_csv(self, data, filepath) -> None

# Usage
rankings_df = client.rankings.get_character_rankings(123).to_dataframe()
rankings_df.to_csv('character_performance.csv')
```

### **3. Query Builder Pattern**

**Current Issue**: Fixed queries, no flexibility  
**Proposed Solution**: Flexible query building

```python
# Advanced query building
reports = await client.report_data.search() \
    .filter_by_guild(guild_id=123) \
    .filter_by_date_range("2025-01-01", "2025-01-31") \
    .filter_by_zone(zone_id=456) \
    .limit(50) \
    .execute()
```

### **4. Caching & Performance**

**Current Issue**: No caching, repeated API calls  
**Proposed Solution**: Intelligent caching system

```python
class CacheManager:
    def cache_static_data(self, data, ttl=3600)  # Game data - long TTL
    def cache_rankings(self, data, ttl=300)      # Rankings - short TTL
    def cache_reports(self, data, ttl=1800)      # Reports - medium TTL
```

## 📋 **Detailed Implementation Plan**

### **PR 1: Character Rankings Implementation** ✅
**Branch**: `v2/character-rankings-api` (PR #4)  
**Status**: ✅ **Completed & Merged**  
**Estimated Size**: Medium

**Tasks**:
1. ✅ Add new GraphQL queries for character rankings
2. ✅ Implement `CharacterRankingsClient` class
3. ✅ Add response models for ranking data
4. ✅ Create unit tests for ranking functionality
5. ✅ Add integration tests with real API calls
6. ✅ Update documentation

**New Methods**:
```python
async def get_character_encounter_rankings(character_id: int, encounter_id: int, **kwargs)
async def get_character_zone_rankings(character_id: int, zone_id: int, **kwargs)  
```

**Implementation Details**:
- Full support for all ranking metrics (dps, hps, playerscore, etc.)
- Comprehensive parameter filtering (role, difficulty, timeframe, etc.)
- 6 new unit tests + integration tests
- Auto-generated Pydantic response models
- Proper GraphQL query generation with ariadne-codegen

### **PR 2: Report Analysis Implementation** ✅
**Branch**: `v2/report-analysis-api` (PR #5)  
**Status**: ✅ **Approved & Ready for Merge**  
**Estimated Size**: Large

**Tasks**:
1. ✅ Add comprehensive report analysis queries
2. ✅ Implement detailed event data retrieval
3. ✅ Add graph and table data methods
4. ✅ Implement report rankings functionality
5. ✅ Add data transformation utilities
6. ✅ Create comprehensive test suite

**New Methods**:
```python
async def get_report_events(code: str, start_time: float = None, end_time: float = None)
async def get_report_graph_data(code: str, data_type: str, **kwargs)
async def get_report_table_data(code: str, data_type: str, **kwargs)
async def get_report_rankings(code: str, encounter_id: int = None)
async def get_report_player_details(code: str, **kwargs)
```

### **PR 3: Advanced Report Search**
**Branch**: `v2/report-search-api`  
**Estimated Size**: Medium

**Tasks**:
1. Implement flexible report search functionality
2. Add filtering by multiple criteria
3. Implement pagination helpers
4. Add query builder pattern
5. Create search result data models

**New Methods**:
```python
async def search_reports(guild_id: int = None, user_id: int = None, zone_id: int = None, **kwargs)
async def get_guild_reports(guild_id: int, limit: int = 50, **kwargs)
async def get_user_reports(user_id: int, limit: int = 50, **kwargs)
```

### **PR 4: Client Architecture Refactor**
**Branch**: `v2/client-architecture-refactor`  
**Estimated Size**: Large (Breaking Changes)

**Tasks**:
1. Create modular client hierarchy
2. Implement specialized client classes
3. Add backwards compatibility layer
4. Update all existing code to new architecture
5. Update documentation and examples
6. Add migration guide

**New Architecture**:
```python
# Before (current)
client = Client(url, headers)
await client.get_character_by_id(123)

# After (new)
client = EsoLogsClient(token)
await client.character_data.get_by_id(123)
```

### **PR 5: Data Transformation Layer**
**Branch**: `v2/data-transformation`  
**Estimated Size**: Medium

**Tasks**:
1. Implement pandas integration
2. Add data export utilities
3. Create transformation helpers
4. Add optional dependency management
5. Update documentation with data analysis examples

### **PR 6: User Account Integration**
**Branch**: `v2/user-account-api`  
**Estimated Size**: Medium

**Tasks**:
1. Implement user data queries
2. Add user profile functionality
3. Implement user's characters and guilds
4. Add authentication-based features

### **PR 7: Progress Race Tracking**
**Branch**: `v2/progress-race-api`  
**Estimated Size**: Small

**Tasks**:
1. Implement progress race data queries
2. Add real-time competition tracking
3. Create progress race data models

## ⏱️ **Implementation Timeline**

### **Week 1-2**: Foundation (PRs 1-3)
- Character Rankings API ✅ **COMPLETED** (PR #4 - In Review)
- Report Analysis API 🚧 **NEXT**
- Advanced Report Search 🚧 **PLANNED**

### **Week 3**: Architecture (PR 4)
- Client Architecture Refactor 🚧 **PLANNED**

### **Week 4**: Enhancement (PRs 5-7)
- Data Transformation Layer 🚧 **PLANNED**
- User Account Integration 🚧 **PLANNED**
- Progress Race Tracking 🚧 **PLANNED**

## 🎯 **Success Metrics**

### **API Coverage**
- **Before Phase 2**: ~20% of GraphQL schema
- **After PR 1**: ~25% of GraphQL schema (Character Rankings added)
- **Target**: ~60-70% of GraphQL schema

### **Code Quality**
- **Test Coverage**: 90%+ for new code
- **Type Coverage**: 95%+ with mypy
- **Documentation**: Complete API docs + examples

### **Performance**
- **Response Time**: <2s for basic queries
- **Caching**: Reduce API calls by 60% for static data
- **Memory**: Efficient handling of large datasets

### **Usability**
- **Intuitive API**: Modular client design
- **Data Export**: pandas integration working
- **Examples**: Complete usage examples for all features

## 🔍 **Risk Assessment**

### **High Risk**
- **Breaking Changes**: Client architecture refactor will break existing code
- **API Complexity**: Report analysis has complex nested data structures

### **Medium Risk** 
- **Performance**: Large datasets might cause memory issues
- **Rate Limiting**: Increased API usage might hit limits

### **Mitigation Strategies**
- **Backwards Compatibility**: Maintain old client alongside new
- **Incremental Rollout**: Implement features in separate PRs
- **Comprehensive Testing**: Unit + integration tests for all features
- **Documentation**: Clear migration guides and examples

## 🚀 **Development Workflow**

1. **Create feature branch** off v2-dev
2. **Implement functionality** with comprehensive tests
3. **Update documentation** and examples
4. **Create PR** to v2-dev for review
5. **Address feedback** and iterate
6. **Merge after approval**

## 📝 **Decision Points for Review**

### **Architecture Decisions**
1. **Client Hierarchy**: Do you approve the modular client design (`client.rankings.get_character_rankings()` vs current flat structure)?
2. **Breaking Changes**: Are you comfortable with PR 4 introducing breaking changes for better architecture?
3. **Data Transformation**: Should pandas integration be built-in or remain optional?

### **Implementation Priority**
1. **PR Order**: Do you agree with the proposed PR sequence (Rankings → Reports → Search → Architecture)?
2. **Timeline**: Does the 4-week timeline seem realistic?
3. **Scope**: Should we add/remove any features from Phase 2?

### **Technical Approach**
1. **Query Builder**: Do you want the fluent query builder pattern or prefer simple method parameters?
2. **Caching**: Should caching be automatic or opt-in?
3. **Backwards Compatibility**: How important is maintaining the current API during transition?

---

**Next Steps**: 
1. Review this plan and provide feedback
2. Approve/modify the proposed approach
3. Begin implementation with PR 1 (Character Rankings)

**Plan Created**: July 9, 2025  
**Author**: Claude Code Assistant