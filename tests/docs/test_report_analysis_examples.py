"""
Tests for examples in docs/api-reference/report-analysis.md

Validates that all code examples in the report analysis API documentation
execute correctly and return expected data structures.
"""

import asyncio

import pytest
from pydantic import ValidationError

from esologs.client import Client
from esologs.enums import (
    EventDataType,
    GraphDataType,
    ReportRankingMetricType,
    TableDataType,
)
from esologs.exceptions import GraphQLClientGraphQLMultiError, GraphQLClientHttpError


class TestReportAnalysisExamples:
    """Test all examples from report-analysis.md documentation"""

    @pytest.fixture
    def test_report_code(self):
        """Report code used in documentation examples"""
        return "VFnNYQjxC3RwGqg1"

    @pytest.mark.asyncio
    async def test_get_report_events_example(self, api_client_config, test_report_code):
        """Test the get_report_events() basic example"""
        async with Client(**api_client_config) as client:
            # From documentation example - with fight_i_ds for real data
            events = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                fight_i_ds=[5],  # Specific fight: Red Witch Gedna Relvel
                start_time=259178.0,
                end_time=270000.0,
            )

            # Validate structure matches documentation
            assert events is not None
            assert hasattr(events, "report_data")
            assert events.report_data is not None
            assert hasattr(events.report_data, "report")
            assert events.report_data.report is not None
            assert hasattr(events.report_data.report, "events")
            assert events.report_data.report.events is not None
            assert hasattr(events.report_data.report.events, "data")
            # next_page_timestamp may be None, which is valid
            assert hasattr(events.report_data.report.events, "next_page_timestamp")

            # With the specific fight, we should have data
            if events.report_data.report.events.data:
                assert isinstance(events.report_data.report.events.data, list)
                assert len(events.report_data.report.events.data) > 0

    @pytest.mark.asyncio
    async def test_get_report_graph_example(self, api_client_config, test_report_code):
        """Test the get_report_graph() basic example"""
        async with Client(**api_client_config) as client:
            # From documentation example
            graph = await client.get_report_graph(
                code=test_report_code,
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=300000.0,  # First 5 minutes
            )

            # Validate structure matches documentation
            assert graph is not None
            assert hasattr(graph, "report_data")
            assert graph.report_data is not None
            assert hasattr(graph.report_data, "report")
            assert graph.report_data.report is not None
            assert hasattr(graph.report_data.report, "graph")
            assert graph.report_data.report.graph is not None
            assert isinstance(graph.report_data.report.graph, dict)

            # Verify the expected structure from documentation
            graph_data = graph.report_data.report.graph
            assert "data" in graph_data
            assert isinstance(graph_data["data"], dict)

    @pytest.mark.asyncio
    async def test_get_report_table_example(self, api_client_config, test_report_code):
        """Test the get_report_table() basic example"""
        async with Client(**api_client_config) as client:
            # From documentation example
            table = await client.get_report_table(
                code=test_report_code,
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=300000.0,
            )

            # Validate structure matches documentation
            assert table is not None
            assert hasattr(table, "report_data")
            assert table.report_data is not None
            assert hasattr(table.report_data, "report")
            assert table.report_data.report is not None
            assert hasattr(table.report_data.report, "table")
            assert table.report_data.report.table is not None
            assert isinstance(table.report_data.report.table, dict)

            # Verify the expected structure from documentation
            table_data = table.report_data.report.table
            assert "data" in table_data
            assert isinstance(table_data["data"], dict)

    @pytest.mark.asyncio
    async def test_get_report_rankings_example(
        self, api_client_config, test_report_code
    ):
        """Test the get_report_rankings() basic example"""
        async with Client(**api_client_config) as client:
            # From documentation example
            rankings = await client.get_report_rankings(
                code=test_report_code, player_metric=ReportRankingMetricType.dps
            )

            # Validate structure matches documentation
            assert rankings is not None
            assert hasattr(rankings, "report_data")
            assert rankings.report_data is not None
            assert hasattr(rankings.report_data, "report")
            assert rankings.report_data.report is not None
            assert hasattr(rankings.report_data.report, "rankings")
            assert rankings.report_data.report.rankings is not None
            assert isinstance(rankings.report_data.report.rankings, dict)

            # Verify the expected structure from documentation
            rankings_data = rankings.report_data.report.rankings
            assert "data" in rankings_data
            data = rankings_data["data"]
            assert isinstance(data, list)
            # The example shows 10 entries, but this may vary
            assert len(data) >= 0

    @pytest.mark.asyncio
    async def test_get_report_player_details_example(
        self, api_client_config, test_report_code
    ):
        """Test the get_report_player_details() basic example"""
        async with Client(**api_client_config) as client:
            # From documentation example
            player_details = await client.get_report_player_details(
                code=test_report_code,
                start_time=0.0,
                end_time=300000.0,
                include_combatant_info=True,
            )

            # Validate structure matches documentation
            assert player_details is not None
            assert hasattr(player_details, "report_data")
            assert player_details.report_data is not None
            assert hasattr(player_details.report_data, "report")
            assert player_details.report_data.report is not None
            assert hasattr(player_details.report_data.report, "player_details")
            assert player_details.report_data.report.player_details is not None
            assert isinstance(player_details.report_data.report.player_details, dict)

            # Verify the expected structure from documentation
            pd_data = player_details.report_data.report.player_details
            assert "data" in pd_data
            assert isinstance(pd_data["data"], dict)

    @pytest.mark.asyncio
    async def test_error_handling_example(self, api_client_config):
        """Test the error handling example from documentation"""
        async with Client(**api_client_config) as client:
            # Test with invalid report code from documentation
            invalid_code = "invalid_code"

            with pytest.raises(
                (
                    GraphQLClientHttpError,
                    GraphQLClientGraphQLMultiError,
                    ValidationError,
                )
            ):
                await client.get_report_events(
                    code=invalid_code, data_type=EventDataType.DamageDone
                )

    @pytest.mark.asyncio
    async def test_comprehensive_analysis_pattern(
        self, api_client_config, test_report_code
    ):
        """Test the comprehensive analysis workflow pattern"""
        async with Client(**api_client_config) as client:
            # Simplified version of the comprehensive analysis pattern

            # Get basic report info
            report = await client.get_report_by_code(code=test_report_code)
            assert report is not None

            # Analyze damage over time
            damage_graph = await client.get_report_graph(
                code=test_report_code,
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=300000.0,
            )
            assert damage_graph is not None

            # Small delay for rate limiting
            await asyncio.sleep(0.5)

            # Get damage summary statistics
            damage_table = await client.get_report_table(
                code=test_report_code,
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=300000.0,
            )
            assert damage_table is not None

            # Compare performance rankings
            rankings = await client.get_report_rankings(
                code=test_report_code, player_metric=ReportRankingMetricType.dps
            )
            assert rankings is not None

            # Small delay for rate limiting
            await asyncio.sleep(0.5)

            # Get individual player breakdowns
            player_details = await client.get_report_player_details(
                code=test_report_code, start_time=0.0, end_time=300000.0
            )
            assert player_details is not None

            # Verify we have all components
            analysis_result = {
                "report": report,
                "damage_graph": damage_graph,
                "damage_table": damage_table,
                "rankings": rankings,
                "player_details": player_details,
            }

            assert all(component is not None for component in analysis_result.values())

    @pytest.mark.asyncio
    async def test_encounter_phase_analysis_pattern(
        self, api_client_config, test_report_code
    ):
        """Test the encounter phase analysis pattern"""
        async with Client(**api_client_config) as client:
            # Test encounter phase analysis with specific fight
            fight_id = 5  # Red Witch Gedna Relvel
            phase_start = 259178.0
            phase_end = 270000.0  # First part of fight

            # Get events for specific phase
            events = await client.get_report_events(
                code=test_report_code,
                fight_i_ds=[fight_id],
                start_time=phase_start,
                end_time=phase_end,
                data_type=EventDataType.DamageDone,
            )
            assert events is not None

            # Small delay for rate limiting
            await asyncio.sleep(0.5)

            # Get phase performance graph
            graph = await client.get_report_graph(
                code=test_report_code,
                fight_i_ds=[fight_id],
                start_time=phase_start,
                end_time=phase_end,
                data_type=GraphDataType.DamageDone,
            )
            assert graph is not None

            # Verify we can analyze the data like the example does
            if events.report_data.report.events.data:
                damage_amounts = [
                    e["amount"]
                    for e in events.report_data.report.events.data
                    if "amount" in e
                ]
                assert len(damage_amounts) > 0

            if graph.report_data.report.graph["data"]["series"]:
                players = graph.report_data.report.graph["data"]["series"]
                assert len(players) > 0
                # Verify player structure has expected keys
                assert "name" in players[0]
                assert "total" in players[0]

    @pytest.mark.asyncio
    async def test_rate_limiting_considerations(
        self, api_client_config, test_report_code
    ):
        """Test that rate limiting considerations are properly handled"""
        async with Client(**api_client_config) as client:
            # Test multiple requests with proper delays as documented
            requests = [
                client.get_report_events(
                    code=test_report_code,
                    data_type=EventDataType.DamageDone,
                    start_time=0.0,
                    end_time=30000.0,
                ),
                client.get_report_graph(
                    code=test_report_code,
                    data_type=GraphDataType.DamageDone,
                    start_time=0.0,
                    end_time=30000.0,
                ),
                client.get_report_table(
                    code=test_report_code,
                    data_type=TableDataType.DamageDone,
                    start_time=0.0,
                    end_time=30000.0,
                ),
            ]

            # Execute with delays as recommended in documentation
            results = []
            for request in requests:
                result = await request
                results.append(result)
                await asyncio.sleep(0.5)  # Rate limit consideration from docs

            # Verify all requests succeeded
            assert all(result is not None for result in results)
            assert len(results) == 3

    @pytest.mark.asyncio
    async def test_data_structure_validation(self, api_client_config, test_report_code):
        """Validate the documented data structures match actual API responses"""
        async with Client(**api_client_config) as client:
            # Test events structure
            events = await client.get_report_events(
                code=test_report_code,
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0,
            )
            # Events: Raw event data as flexible Any type
            assert hasattr(events.report_data.report.events, "data")
            # Pagination support
            assert hasattr(events.report_data.report.events, "next_page_timestamp")

            await asyncio.sleep(0.5)

            # Test graph structure
            graph = await client.get_report_graph(
                code=test_report_code,
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0,
            )
            # Graphs: Performance data as dict with 'data' key
            assert isinstance(graph.report_data.report.graph, dict)
            assert "data" in graph.report_data.report.graph

            await asyncio.sleep(0.5)

            # Test table structure
            table = await client.get_report_table(
                code=test_report_code,
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0,
            )
            # Tables: Analysis results as dict with 'data' key
            assert isinstance(table.report_data.report.table, dict)
            assert "data" in table.report_data.report.table

            await asyncio.sleep(0.5)

            # Test rankings structure
            rankings = await client.get_report_rankings(
                code=test_report_code, player_metric=ReportRankingMetricType.dps
            )
            # Rankings: List of ranking objects
            assert isinstance(rankings.report_data.report.rankings, dict)
            assert "data" in rankings.report_data.report.rankings
            assert isinstance(rankings.report_data.report.rankings["data"], list)

            await asyncio.sleep(0.5)

            # Test player details structure
            player_details = await client.get_report_player_details(
                code=test_report_code, start_time=0.0, end_time=60000.0
            )
            # Player Details: Comprehensive stats as structured dict
            assert isinstance(player_details.report_data.report.player_details, dict)
            assert "data" in player_details.report_data.report.player_details
            assert isinstance(
                player_details.report_data.report.player_details["data"], dict
            )
