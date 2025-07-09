# python-esologs
A Python frontend for the ![https://www.esologs.com/](esologs) API. 

Note: This project is early. Currently only contains a basic Python script to pull slices of data from a subset of filters.

Requires at least Python >= 3.6. Tested on MacOS, but should work on all platforms.


# Quickstart
---
## Install
1. Clone this repo
2. Create a virtual environment (optional)
3. Install dependencies 
```Bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Obtain API Key
Set V1 Client Name and generate a key in the Web API section at the bottom of ![this page](https://www.esologs.com/profile).

## Download Data
Example
```Bash
$ cd ./scripts
$ python pull_data.py --target-spec stamina --target-class nightblade --target-patch 34 --output-directory ./test --api-key my_esologs_api_key
```
Output:
```Text
[update 34] stamina nightblade
 * found 6 parses over 40k dps
 * query: https://www.esologs.com:443/v1/rankings/encounter/3009?metric=dps&partition=13&class=2&spec=3&page=1&includeCombatantInfo=true&api_key=
```
![Output file](/examples/34-stamina-nightblade.json)
# V1 API Archive

This branch (`v1-api`) preserves the original ESO Logs v1 API implementation.

## ⚠️ Deprecation Notice

**The ESO Logs v1 API is deprecated and this code is preserved for historical reference only.**

- **Status**: Deprecated (ESO Logs v1 API is no longer maintained)
- **Recommendation**: Use the v2 API implementation in the `v2-dev` branch
- **Purpose**: Historical preservation and migration reference

## What's in This Branch

This branch contains the original Python implementation that used the ESO Logs v1 API:

- `scripts/pull_data.py` - Main v1 API data extraction script
- `config.py` - Configuration for v1 API endpoints
- `examples/` - Sample output from v1 API calls
- Basic requirements.txt with minimal dependencies

## v1 vs v2 API Differences

| Feature | v1 API (This Branch) | v2 API (v2-dev Branch) |
|---------|---------------------|-------------------------|
| **API Type** | REST API | GraphQL API |
| **Authentication** | API Key | OAuth2 Client Credentials |
| **Data Format** | Simple JSON responses | Structured GraphQL schemas |
| **Code Generation** | Manual implementation | Auto-generated from schema |
| **Type Safety** | Basic Python types | Pydantic models with validation |
| **Query Flexibility** | Fixed endpoints | Flexible GraphQL queries |
| **Maintenance** | ❌ Deprecated | ✅ Active development |

## Migration Path

If you're using this v1 code, please migrate to the v2 implementation:

1. **Switch to v2-dev branch**: `git checkout v2-dev`
2. **Follow v2 setup instructions**: See README.md in v2-dev branch
3. **Update authentication**: Use OAuth2 instead of API keys
4. **Rewrite queries**: Use GraphQL client instead of REST calls

## Historical Context

This code was created when ESO Logs only provided a v1 REST API. The v2 GraphQL API provides:
- Better performance and flexibility
- Comprehensive data access
- Modern authentication and security
- Type-safe client generation
- Active maintenance and support

## Preservation Date

This branch was created on July 9, 2025 to preserve the v1 API implementation before migrating the main branch to v2 API code.

---

**For current development, use the `v2-dev` branch which implements the modern ESO Logs v2 GraphQL API.**
