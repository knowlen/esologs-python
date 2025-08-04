"""Unit tests for report analysis functionality."""

from unittest.mock import AsyncMock, Mock

import pytest

from esologs._generated.enums import (
    EventDataType,
    GraphDataType,
    HostilityType,
    KillType,
    RankingCompareType,
    RankingTimeframeType,
    ReportRankingMetricType,
    TableDataType,
    ViewType,
)
from esologs._generated.get_report_events import GetReportEvents
from esologs._generated.get_report_graph import GetReportGraph
from esologs._generated.get_report_player_details import GetReportPlayerDetails
from esologs._generated.get_report_rankings import GetReportRankings
from esologs._generated.get_report_table import GetReportTable
from esologs.client import Client


class TestReportAnalysis:
    """Test class for report analysis methods."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client for testing."""
        client = Mock(spec=Client)
        client.execute = AsyncMock()
        client.get_data = Mock()
        return client

    @pytest.fixture
    def mock_report_events_response(self):
        """Mock response for report events."""
        return {
            "reportData": {
                "report": {
                    "events": {
                        "data": [
                            {
                                "timestamp": 1634567890000,
                                "type": "damage",
                                "sourceID": 1,
                                "targetID": 2,
                                "abilityGameID": 12345,
                                "amount": 5000,
                                "hitType": 1,
                            },
                            {
                                "timestamp": 1634567895000,
                                "type": "healing",
                                "sourceID": 3,
                                "targetID": 1,
                                "abilityGameID": 67890,
                                "amount": 3000,
                                "hitType": 1,
                            },
                        ],
                        "nextPageTimestamp": 1634567900000,
                    }
                }
            }
        }

    @pytest.fixture
    def mock_report_graph_response(self):
        """Mock response for report graph data."""
        return {
            "reportData": {
                "report": {
                    "graph": {
                        "startTime": 1634567890000,
                        "endTime": 1634567950000,
                        "series": [
                            {
                                "name": "Player 1",
                                "data": [
                                    [1634567890000, 5000],
                                    [1634567895000, 5500],
                                    [1634567900000, 6000],
                                ],
                            }
                        ],
                    }
                }
            }
        }

    @pytest.fixture
    def mock_report_table_response(self):
        """Mock response for report table data."""
        return {
            "reportData": {
                "report": {
                    "table": {
                        "totalTime": 60000,
                        "itemLevel": 160,
                        "composition": [
                            {
                                "name": "Player 1",
                                "id": 1,
                                "guid": 12345,
                                "type": "Dragonknight",
                                "specs": ["Dragonknight"],
                                "minItemLevel": 160,
                                "maxItemLevel": 160,
                                "potionUse": 2,
                                "healthstoneUse": 0,
                                "total": 300000,
                                "activeTime": 55000,
                                "activeTimeReduced": 55000,
                            }
                        ],
                    }
                }
            }
        }

    @pytest.fixture
    def mock_report_rankings_response(self):
        """Mock response for report rankings."""
        return {
            "reportData": {
                "report": {
                    "rankings": {
                        "playerRankings": [
                            {
                                "name": "Player 1",
                                "total": 300000,
                                "rank": 1,
                                "rankPercent": 95.5,
                                "classColor": "c79c6e",
                                "spec": "Dragonknight",
                                "role": "DPS",
                            }
                        ],
                        "fightCount": 1,
                        "totalTime": 60000,
                    }
                }
            }
        }

    @pytest.fixture
    def mock_report_player_details_response(self):
        """Mock response for report player details."""
        return {
            "reportData": {
                "report": {
                    "playerDetails": {
                        "healers": [],
                        "tanks": [],
                        "dps": [
                            {
                                "name": "Player 1",
                                "id": 1,
                                "guid": 12345,
                                "type": "Dragonknight",
                                "specs": ["Dragonknight"],
                                "minItemLevel": 160,
                                "maxItemLevel": 160,
                                "potionUse": 2,
                                "healthstoneUse": 0,
                            }
                        ],
                    }
                }
            }
        }

    @pytest.mark.asyncio
    async def test_get_report_events_basic(
        self, mock_client, mock_report_events_response
    ):
        """Test basic report events functionality."""
        # Setup
        mock_client.get_data.return_value = mock_report_events_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_report_events(code="ABC123")

        # Assertions
        assert isinstance(result, GetReportEvents)
        assert result.report_data is not None
        assert result.report_data.report is not None
        assert result.report_data.report.events is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getReportEvents"
        assert call_args[1]["variables"]["code"] == "ABC123"

    @pytest.mark.asyncio
    async def test_get_report_events_with_params(
        self, mock_client, mock_report_events_response
    ):
        """Test report events with parameters."""
        # Setup
        mock_client.get_data.return_value = mock_report_events_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with parameters
        result = await client.get_report_events(
            code="ABC123",
            data_type=EventDataType.DamageDone,
            start_time=1634567890000,
            end_time=1634567950000,
            encounter_id=27,
            limit=100,
            hostility_type=HostilityType.Enemies,
            kill_type=KillType.Kills,
        )

        # Assertions
        assert isinstance(result, GetReportEvents)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]
        assert variables["code"] == "ABC123"
        assert variables["dataType"] == EventDataType.DamageDone
        assert variables["startTime"] == 1634567890000
        assert variables["endTime"] == 1634567950000
        assert variables["encounterID"] == 27
        assert variables["limit"] == 100
        assert variables["hostilityType"] == HostilityType.Enemies
        assert variables["killType"] == KillType.Kills

    @pytest.mark.asyncio
    async def test_get_report_graph_basic(
        self, mock_client, mock_report_graph_response
    ):
        """Test basic report graph functionality."""
        # Setup
        mock_client.get_data.return_value = mock_report_graph_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_report_graph(code="ABC123")

        # Assertions
        assert isinstance(result, GetReportGraph)
        assert result.report_data is not None
        assert result.report_data.report is not None
        assert result.report_data.report.graph is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getReportGraph"
        assert call_args[1]["variables"]["code"] == "ABC123"

    @pytest.mark.asyncio
    async def test_get_report_graph_with_params(
        self, mock_client, mock_report_graph_response
    ):
        """Test report graph with parameters."""
        # Setup
        mock_client.get_data.return_value = mock_report_graph_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with parameters
        result = await client.get_report_graph(
            code="ABC123",
            data_type=GraphDataType.DamageDone,
            start_time=1634567890000,
            end_time=1634567950000,
            encounter_id=27,
            view_by=ViewType.Source,
        )

        # Assertions
        assert isinstance(result, GetReportGraph)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]
        assert variables["code"] == "ABC123"
        assert variables["dataType"] == GraphDataType.DamageDone
        assert variables["startTime"] == 1634567890000
        assert variables["endTime"] == 1634567950000
        assert variables["encounterID"] == 27
        assert variables["viewBy"] == ViewType.Source

    @pytest.mark.asyncio
    async def test_get_report_table_basic(
        self, mock_client, mock_report_table_response
    ):
        """Test basic report table functionality."""
        # Setup
        mock_client.get_data.return_value = mock_report_table_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_report_table(code="ABC123")

        # Assertions
        assert isinstance(result, GetReportTable)
        assert result.report_data is not None
        assert result.report_data.report is not None
        assert result.report_data.report.table is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getReportTable"
        assert call_args[1]["variables"]["code"] == "ABC123"

    @pytest.mark.asyncio
    async def test_get_report_table_with_params(
        self, mock_client, mock_report_table_response
    ):
        """Test report table with parameters."""
        # Setup
        mock_client.get_data.return_value = mock_report_table_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with parameters
        result = await client.get_report_table(
            code="ABC123",
            data_type=TableDataType.DamageDone,
            start_time=1634567890000,
            end_time=1634567950000,
            encounter_id=27,
            view_by=ViewType.Source,
        )

        # Assertions
        assert isinstance(result, GetReportTable)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]
        assert variables["code"] == "ABC123"
        assert variables["dataType"] == TableDataType.DamageDone
        assert variables["startTime"] == 1634567890000
        assert variables["endTime"] == 1634567950000
        assert variables["encounterID"] == 27
        assert variables["viewBy"] == ViewType.Source

    @pytest.mark.asyncio
    async def test_get_report_rankings_basic(
        self, mock_client, mock_report_rankings_response
    ):
        """Test basic report rankings functionality."""
        # Setup
        mock_client.get_data.return_value = mock_report_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_report_rankings(code="ABC123")

        # Assertions
        assert isinstance(result, GetReportRankings)
        assert result.report_data is not None
        assert result.report_data.report is not None
        assert result.report_data.report.rankings is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getReportRankings"
        assert call_args[1]["variables"]["code"] == "ABC123"

    @pytest.mark.asyncio
    async def test_get_report_rankings_with_params(
        self, mock_client, mock_report_rankings_response
    ):
        """Test report rankings with parameters."""
        # Setup
        mock_client.get_data.return_value = mock_report_rankings_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with parameters
        result = await client.get_report_rankings(
            code="ABC123",
            encounter_id=27,
            player_metric=ReportRankingMetricType.dps,
            compare=RankingCompareType.Rankings,
            timeframe=RankingTimeframeType.Today,
            difficulty=125,
        )

        # Assertions
        assert isinstance(result, GetReportRankings)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]
        assert variables["code"] == "ABC123"
        assert variables["encounterID"] == 27
        assert variables["playerMetric"] == ReportRankingMetricType.dps
        assert variables["compare"] == RankingCompareType.Rankings
        assert variables["timeframe"] == RankingTimeframeType.Today
        assert variables["difficulty"] == 125

    @pytest.mark.asyncio
    async def test_get_report_player_details_basic(
        self, mock_client, mock_report_player_details_response
    ):
        """Test basic report player details functionality."""
        # Setup
        mock_client.get_data.return_value = mock_report_player_details_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test
        result = await client.get_report_player_details(code="ABC123")

        # Assertions
        assert isinstance(result, GetReportPlayerDetails)
        assert result.report_data is not None
        assert result.report_data.report is not None
        assert result.report_data.report.player_details is not None

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        assert call_args[1]["operation_name"] == "getReportPlayerDetails"
        assert call_args[1]["variables"]["code"] == "ABC123"

    @pytest.mark.asyncio
    async def test_get_report_player_details_with_params(
        self, mock_client, mock_report_player_details_response
    ):
        """Test report player details with parameters."""
        # Setup
        mock_client.get_data.return_value = mock_report_player_details_response

        client = Client(url="https://test.com", headers={})
        client.execute = mock_client.execute
        client.get_data = mock_client.get_data

        # Test with parameters
        result = await client.get_report_player_details(
            code="ABC123",
            encounter_id=27,
            start_time=1634567890000,
            end_time=1634567950000,
            difficulty=125,
            kill_type=KillType.Kills,
            translate=True,
            include_combatant_info=True,
        )

        # Assertions
        assert isinstance(result, GetReportPlayerDetails)

        # Check that execute was called with correct parameters
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args
        variables = call_args[1]["variables"]
        assert variables["code"] == "ABC123"
        assert variables["encounterID"] == 27
        assert variables["startTime"] == 1634567890000
        assert variables["endTime"] == 1634567950000
        assert variables["difficulty"] == 125
        assert variables["killType"] == KillType.Kills
        assert variables["translate"] is True
        assert variables["includeCombatantInfo"] is True
