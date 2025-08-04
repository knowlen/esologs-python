# Using the GraphQL Client Directly

While the ESO Logs Python client provides 100% coverage of the available top-level API methods, some advanced features are only accessible through nested GraphQL queries. This guide shows you how to access the underlying GraphQL client for these edge cases.

## What's Not Exposed?

The following GraphQL schema features aren't available through the Python client's convenience methods:

### 1. Encounter-specific Character Rankings
The `Encounter.characterRankings` field provides additional filtering options not available in the standard character ranking methods:

- `externalBuffs` - Filter rankings by external buff usage
- `hardModeLevel` - Filter by specific hard mode levels (0-4)
- `leaderboard` - Include/exclude ranks without backing logs

### 2. Why These Aren't Exposed

These fields require nested queries through `worldData.zones.encounters`, making them more complex to use and less commonly needed. The ESO Logs API design focuses on top-level query methods for the most common use cases.

## Accessing the GraphQL Client

The ESO Logs Python client is built on `gql`, so you can access the underlying GraphQL client for custom queries:

```python
from gql import gql
from esologs import Client
from esologs.auth import get_access_token

async def custom_encounter_rankings():
    token = get_access_token()

    # Use the standard client
    async with Client(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    ) as client:

        # Access the underlying GraphQL transport
        # Note: This is the internal implementation detail
        query = gql("""
            query getEncounterRankings($zoneId: Int!, $encounterId: Int!) {
                worldData {
                    zone(id: $zoneId) {
                        encounters {
                            id
                            name
                            characterRankings(
                                externalBuffs: Exclude
                                hardModeLevel: Highest
                                leaderboard: LogsOnly
                            )
                        }
                    }
                }
            }
        """)

        # Execute using the client's session
        result = await client.session.execute(
            query,
            variable_values={
                "zoneId": 38,  # Dreadsail Reef
                "encounterId": 88
            }
        )

        return result
```

## Alternative: Direct GraphQL Client

For complete control, you can create your own GraphQL client:

```python
from gql import Client as GQLClient, gql
from gql.transport.aiohttp import AIOHTTPTransport
from esologs.auth import get_access_token

async def direct_graphql_query():
    token = get_access_token()

    # Create your own transport
    transport = AIOHTTPTransport(
        url="https://www.esologs.com/api/v2/client",
        headers={"Authorization": f"Bearer {token}"}
    )

    # Create a GraphQL client
    async with GQLClient(
        transport=transport,
        fetch_schema_from_transport=True
    ) as session:

        # Your custom query
        query = gql("""
            query {
                worldData {
                    zones {
                        id
                        name
                        encounters {
                            id
                            name
                            characterRankings(
                                metric: dps
                                difficulty: 122
                                externalBuffs: Exclude
                            )
                        }
                    }
                }
            }
        """)

        result = await session.execute(query)
        return result
```

## When to Use Direct GraphQL

Consider using direct GraphQL queries when you need:

1. **Advanced Ranking Filters**: External buffs, hard mode levels, leaderboard filtering
2. **Nested Data Fetching**: Complex queries that fetch related data in one request
3. **Schema Exploration**: Discovering what other fields might be available
4. **Custom Field Selection**: Optimizing requests by selecting only needed fields

## Best Practices

1. **Use the Python Client First**: It handles authentication, rate limiting, and provides type safety
2. **Fall Back to GraphQL When Needed**: Only use direct queries for features not exposed
3. **Share Your Use Cases**: If you frequently need direct GraphQL access, let us know - we may add it to the client
4. **Cache Results**: These complex queries can be expensive - cache when appropriate

## Future Enhancements

We're considering adding:
- An `execute_graphql()` method for custom queries
- Support for the most requested nested fields
- Query builder helpers for common patterns

If you have specific needs, please [open an issue](https://github.com/knowlen/esologs-python/issues) describing your use case!
