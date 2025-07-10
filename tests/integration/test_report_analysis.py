"""Integration tests for Report Analysis API methods."""

import asyncio
import pytest
import os
from typing import Optional

from esologs.client import Client
from esologs.enums import (
    EventDataType,
    GraphDataType,
    TableDataType,
    ReportRankingMetricType,
    HostilityType,
    ViewType
)
from access_token import get_access_token


# Fixtures are now centralized in conftest.py


class TestReportAnalysisIntegration:
    """Integration tests for report analysis functionality."""

    @pytest.mark.asyncio
    async def test_get_report_events_basic(self, client, test_data):
        """Test basic report events retrieval."""
        async with client:
            response = await client.get_report_events(
                code=test_data["report_code"],
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0  # First minute
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data and response.report_data.report:
                assert response.report_data.report.events is not None

    @pytest.mark.asyncio
    async def test_get_report_events_with_time_range(self, client, test_data):
        """Test report events with time range filtering."""
        async with client:
            response = await client.get_report_events(
                code=test_data["report_code"],
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0  # First minute
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_events_different_data_types(self, client, test_data):
        """Test report events with different data types."""
        data_types_to_test = [
            EventDataType.DamageDone,
            EventDataType.Healing,
            EventDataType.Deaths
        ]
        
        async with client:
            for data_type in data_types_to_test:
                response = await client.get_report_events(
                    code=test_data["report_code"],
                    data_type=data_type,
                    start_time=0.0,
                    end_time=60000.0
                )
                
                assert response is not None
                assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_graph_basic(self, client, test_data):
        """Test basic report graph data retrieval."""
        async with client:
            response = await client.get_report_graph(
                code=test_data["report_code"],
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data and response.report_data.report:
                assert response.report_data.report.graph is not None

    @pytest.mark.asyncio
    async def test_get_report_graph_with_filters(self, client, test_data):
        """Test report graph with additional filters."""
        async with client:
            response = await client.get_report_graph(
                code=test_data["report_code"],
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0,
                hostility_type=HostilityType.Enemies
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_graph_different_data_types(self, client, test_data):
        """Test report graph with different data types."""
        data_types_to_test = [
            GraphDataType.DamageDone,
            GraphDataType.Healing,
            GraphDataType.DamageTaken
        ]
        
        async with client:
            for data_type in data_types_to_test:
                response = await client.get_report_graph(
                    code=test_data["report_code"],
                    data_type=data_type,
                    start_time=0.0,
                    end_time=60000.0
                )
                
                assert response is not None
                assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_table_basic(self, client, test_data):
        """Test basic report table data retrieval."""
        async with client:
            response = await client.get_report_table(
                code=test_data["report_code"],
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data and response.report_data.report:
                assert response.report_data.report.table is not None

    @pytest.mark.asyncio
    async def test_get_report_table_with_filters(self, client, test_data):
        """Test report table with additional filters."""
        async with client:
            response = await client.get_report_table(
                code=test_data["report_code"],
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0,
                hostility_type=HostilityType.Enemies
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_table_different_data_types(self, client, test_data):
        """Test report table with different data types."""
        data_types_to_test = [
            TableDataType.DamageDone,
            TableDataType.Healing,
            TableDataType.Deaths
        ]
        
        async with client:
            for data_type in data_types_to_test:
                response = await client.get_report_table(
                    code=test_data["report_code"],
                    data_type=data_type,
                    start_time=0.0,
                    end_time=60000.0
                )
                
                assert response is not None
                assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_rankings_basic(self, client, test_data):
        """Test basic report rankings retrieval."""
        async with client:
            response = await client.get_report_rankings(
                code=test_data["report_code"],
                player_metric=ReportRankingMetricType.dps
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data and response.report_data.report:
                assert response.report_data.report.rankings is not None

    @pytest.mark.asyncio
    async def test_get_report_rankings_with_encounter(self, client, test_data):
        """Test report rankings with specific encounter."""
        async with client:
            response = await client.get_report_rankings(
                code=test_data["report_code"],
                encounter_id=test_data["encounter_id"],
                player_metric=ReportRankingMetricType.dps
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_rankings_different_metrics(self, client, test_data):
        """Test report rankings with different metrics."""
        metrics_to_test = [
            ReportRankingMetricType.dps,
            ReportRankingMetricType.hps,
            ReportRankingMetricType.playerscore
        ]
        
        async with client:
            for metric in metrics_to_test:
                response = await client.get_report_rankings(
                    code=test_data["report_code"],
                    player_metric=metric
                )
                
                assert response is not None
                assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_get_report_player_details_basic(self, client, test_data):
        """Test basic report player details retrieval."""
        async with client:
            response = await client.get_report_player_details(
                code=test_data["report_code"],
                start_time=0.0,
                end_time=60000.0
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')
            if response.report_data and response.report_data.report:
                assert response.report_data.report.player_details is not None

    @pytest.mark.asyncio
    async def test_get_report_player_details_with_filters(self, client, test_data):
        """Test report player details with additional filters."""
        async with client:
            response = await client.get_report_player_details(
                code=test_data["report_code"],
                start_time=0.0,
                end_time=60000.0
            )
            
            assert response is not None
            assert hasattr(response, 'report_data')

    @pytest.mark.asyncio
    async def test_report_analysis_with_invalid_code(self, client):
        """Test report analysis methods with invalid report code."""
        invalid_code = "ABCDEfghij123456"  # Valid format but non-existent report
        
        async with client:
            # Test that methods handle invalid codes by raising appropriate errors
            try:
                response = await client.get_report_events(
                    code=invalid_code,
                    data_type=EventDataType.DamageDone,
                    start_time=0.0,
                    end_time=60000.0
                )
                # If no exception, check response structure
                assert response is not None
                assert hasattr(response, 'report_data')
            except Exception as e:
                # Expected to raise GraphQLQueryError for non-existent report
                assert "report" in str(e).lower() and ("exist" in str(e).lower() or "not found" in str(e).lower())

    @pytest.mark.asyncio
    @pytest.mark.timeout(60)  # 60 second timeout for comprehensive test
    async def test_report_analysis_comprehensive_workflow(self, client, test_data):
        """Test comprehensive report analysis workflow."""
        async with client:
            # Get basic report info
            report_info = await client.get_report_by_code(code=test_data["report_code"])
            assert report_info is not None
            
            # Get events data
            events = await client.get_report_events(
                code=test_data["report_code"],
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            assert events is not None
            
            # Get graph data
            graph = await client.get_report_graph(
                code=test_data["report_code"],
                data_type=GraphDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            assert graph is not None
            
            # Get table data
            table = await client.get_report_table(
                code=test_data["report_code"],
                data_type=TableDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            assert table is not None
            
            # Get rankings
            rankings = await client.get_report_rankings(
                code=test_data["report_code"],
                player_metric=ReportRankingMetricType.dps
            )
            assert rankings is not None
            
            # Get player details
            player_details = await client.get_report_player_details(
                code=test_data["report_code"],
                start_time=0.0,
                end_time=60000.0
            )
            assert player_details is not None


if __name__ == "__main__":
    # Run a simple test if executed directly
    async def main():
        client = Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {get_access_token()}"}
        )
        
        async with client:
            response = await client.get_report_events(
                code="VfxqaX47HGC98rAp",
                data_type=EventDataType.DamageDone,
                start_time=0.0,
                end_time=60000.0
            )
            print("Report Analysis Integration Test Result:", response)
    
    asyncio.run(main())