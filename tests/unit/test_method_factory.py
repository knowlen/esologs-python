"""
Unit tests for method factory functions.
"""

from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from esologs._generated.base_model import UNSET
from esologs._generated.get_abilities import GetAbilities
from esologs._generated.get_ability import GetAbility
from esologs._generated.get_world_data import GetWorldData
from esologs.method_factory import (
    create_complex_method,
    create_method_with_builder,
    create_no_params_getter,
    create_paginated_getter,
    create_simple_getter,
)
from esologs.queries import QUERIES


class MockReturnType(MagicMock):
    """Mock return type that implements model_validate."""

    @classmethod
    def model_validate(cls, obj):
        """Mock model_validate method."""
        instance = cls()
        instance._data = obj
        return instance


class MockClient:
    """Mock client for testing factory methods."""

    def __init__(self):
        self.execute = AsyncMock()
        self.get_data = Mock()


class TestMethodFactory:
    """Test suite for method factory functions."""

    @pytest.fixture
    def mock_client(self):
        """Create a mock client instance."""
        return MockClient()

    @pytest.fixture
    def mock_response_data(self):
        """Mock response data for testing."""
        return {
            "gameData": {
                "ability": {
                    "id": 123,
                    "name": "Test Ability",
                    "icon": "test.png",
                    "description": "Test description",
                }
            }
        }

    @pytest.mark.asyncio
    async def test_create_simple_getter(self, mock_client, mock_response_data):
        """Test create_simple_getter factory."""
        # Setup
        mock_client.get_data.return_value = mock_response_data

        # Create method
        method = create_simple_getter(
            operation_name="getAbility", return_type=GetAbility, id_param_name="id"
        )

        # Bind method to mock client
        bound_method = method.__get__(mock_client, MockClient)

        # Execute
        result = await bound_method(id=123)

        # Verify
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args

        assert call_args[1]["query"] == QUERIES["getAbility"]
        assert call_args[1]["operation_name"] == "getAbility"
        assert call_args[1]["variables"] == {"id": 123}

        mock_client.get_data.assert_called_once()
        assert isinstance(result, GetAbility)

    @pytest.mark.asyncio
    async def test_create_simple_getter_with_custom_param_name(self, mock_client):
        """Test create_simple_getter with custom parameter name."""
        # Setup
        mock_client.get_data.return_value = {"guildData": {"guild": {"id": 456}}}

        # Create method with custom param name
        method = create_simple_getter(
            operation_name="getGuildById",
            return_type=MockReturnType,
            id_param_name="guildId",
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(id=456)

        # Verify correct parameter mapping
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables == {"guildId": 456}

    @pytest.mark.asyncio
    async def test_create_no_params_getter(self, mock_client):
        """Test create_no_params_getter factory."""
        # Setup
        mock_client.get_data.return_value = {"worldData": {}}

        # Create method
        method = create_no_params_getter(
            operation_name="getWorldData", return_type=MockReturnType
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method()

        # Verify
        mock_client.execute.assert_called_once()
        call_args = mock_client.execute.call_args

        assert call_args[1]["query"] == QUERIES["getWorldData"]
        assert call_args[1]["operation_name"] == "getWorldData"
        assert call_args[1]["variables"] == {}

    @pytest.mark.asyncio
    async def test_create_paginated_getter(self, mock_client):
        """Test create_paginated_getter factory."""
        # Setup
        mock_client.get_data.return_value = {
            "gameData": {
                "abilities": {
                    "data": [],
                    "total": 100,
                    "per_page": 10,
                    "current_page": 1,
                }
            }
        }

        # Create method
        method = create_paginated_getter(
            operation_name="getAbilities", return_type=MockReturnType
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(limit=20, page=2)

        # Verify
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables == {"limit": 20, "page": 2}

    @pytest.mark.asyncio
    async def test_create_paginated_getter_with_extra_params(self, mock_client):
        """Test create_paginated_getter with extra parameters."""
        # Setup
        mock_client.get_data.return_value = {"gameData": {"classes": []}}

        # Create method with extra params
        method = create_paginated_getter(
            operation_name="getClasses",
            return_type=MockReturnType,
            extra_params={"faction_id": int, "zone_id": int},
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(limit=10, page=1, faction_id=1, zone_id=2)

        # Verify all parameters are passed
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables == {"limit": 10, "page": 1, "faction_id": 1, "zone_id": 2}

    @pytest.mark.asyncio
    async def test_create_paginated_getter_with_unset_params(self, mock_client):
        """Test paginated getter handles UNSET correctly."""
        # Setup
        mock_client.get_data.return_value = {"gameData": {"items": {"data": []}}}

        # Create method
        method = create_paginated_getter(
            operation_name="getItems", return_type=MockReturnType
        )

        # Bind and execute with UNSET params
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(limit=UNSET, page=5)

        # Verify UNSET is preserved
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables["limit"] is UNSET
        assert variables["page"] == 5

    @pytest.mark.asyncio
    async def test_create_complex_method(self, mock_client):
        """Test create_complex_method factory."""
        # Setup
        mock_client.get_data.return_value = {"reportData": {"report": {"events": {}}}}

        # Create method
        method = create_complex_method(
            operation_name="getReportEvents",
            return_type=MockReturnType,
            required_params={"code": str},
            optional_params={"start_time": float, "end_time": float, "limit": int},
            param_mapping={"start_time": "startTime", "end_time": "endTime"},
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(
            code="ABC123", start_time=1000.0, end_time=2000.0, limit=UNSET
        )

        # Verify parameter mapping
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables == {
            "code": "ABC123",
            "startTime": 1000.0,
            "endTime": 2000.0,
            "limit": UNSET,
        }

    @pytest.mark.asyncio
    async def test_create_complex_method_missing_required(self, mock_client):
        """Test complex method raises error for missing required params."""
        # Create method
        method = create_complex_method(
            operation_name="getReportEvents",
            return_type=MockReturnType,
            required_params={"code": str, "report_id": int},
            optional_params={},
        )

        # Bind method
        bound_method = method.__get__(mock_client, MockClient)

        # Should raise TypeError for missing required param
        with pytest.raises(TypeError, match="Missing required parameter: report_id"):
            await bound_method(code="ABC123")

    @pytest.mark.asyncio
    async def test_create_method_with_builder(self, mock_client):
        """Test create_method_with_builder factory."""
        # Setup
        mock_client.get_data.return_value = {"data": {}}

        # Create custom builder function
        def custom_builder(**kwargs: Any) -> Dict[str, object]:
            # Transform parameters
            result = {}
            if "user_id" in kwargs:
                result["userID"] = kwargs["user_id"]
            if "start_date" in kwargs:
                result["startTime"] = kwargs["start_date"] * 1000  # Convert to ms
            return result

        # Create method - use an existing query name
        method = create_method_with_builder(
            operation_name="getReports",
            return_type=MockReturnType,
            param_builder=custom_builder,
        )

        # Bind and execute
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(user_id=123, start_date=1640995200)

        # Verify builder was used
        variables = mock_client.execute.call_args[1]["variables"]
        assert variables == {"userID": 123, "startTime": 1640995200000}

    def test_method_metadata(self):
        """Test that factory methods set proper metadata."""
        # Test simple getter
        method = create_simple_getter(
            operation_name="getAbility", return_type=GetAbility
        )
        assert method.__name__ == "get_ability"
        assert "Get GetAbility by id" in method.__doc__

        # Test no params getter
        method = create_no_params_getter(
            operation_name="getWorldData", return_type=GetWorldData
        )
        assert method.__name__ == "get_world_data"
        assert "Get GetWorldData" in method.__doc__

        # Test paginated getter
        method = create_paginated_getter(
            operation_name="getAbilities", return_type=GetAbilities
        )
        assert method.__name__ == "get_abilities"
        assert "Get paginated GetAbilities" in method.__doc__

    @pytest.mark.asyncio
    async def test_kwargs_passthrough(self, mock_client):
        """Test that extra kwargs are passed through to execute."""
        # Setup
        mock_client.get_data.return_value = {"data": {}}

        # Create method
        method = create_simple_getter(
            operation_name="getAbility", return_type=MockReturnType
        )

        # Bind and execute with extra kwargs
        bound_method = method.__get__(mock_client, MockClient)
        await bound_method(id=123, custom_header="value", timeout=30)

        # Verify kwargs were passed through
        call_kwargs = mock_client.execute.call_args[1]
        assert "custom_header" in call_kwargs
        assert call_kwargs["custom_header"] == "value"
        assert "timeout" in call_kwargs
        assert call_kwargs["timeout"] == 30
