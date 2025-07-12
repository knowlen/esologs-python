"""
Tests for examples in docs/api-reference/system.md

Validates that all code examples in the system API documentation 
execute correctly and return expected data structures.
"""

import pytest
import asyncio
import httpx
from esologs.client import Client
from access_token import get_access_token
from esologs.exceptions import GraphQLClientHttpError, GraphQLClientGraphQLMultiError, GraphQLClientGraphQLError
from pydantic import ValidationError


class TestSystemExamples:
    """Test all examples from system.md documentation"""

    @pytest.mark.asyncio
    async def test_check_rate_limits_example(self, api_client_config):
        """Test the get_rate_limit_data() basic example"""
        async with Client(**api_client_config) as client:
            # Check current rate limit status
            rate_limit = await client.get_rate_limit_data()
            
            # Validate response structure
            assert hasattr(rate_limit, 'rate_limit_data')
            assert hasattr(rate_limit.rate_limit_data, 'points_spent_this_hour')
            assert hasattr(rate_limit.rate_limit_data, 'limit_per_hour')
            
            # Validate data types
            assert isinstance(rate_limit.rate_limit_data.points_spent_this_hour, (int, float))
            assert isinstance(rate_limit.rate_limit_data.limit_per_hour, int)
            assert rate_limit.rate_limit_data.limit_per_hour == 18000

    @pytest.mark.asyncio
    async def test_authentication_error_handling_example(self, api_client_config):
        """Test authentication error handling patterns"""
        # Test with valid credentials (should succeed)
        async with Client(**api_client_config) as client:
            try:
                rate_limit = await client.get_rate_limit_data()
                # Should succeed with valid credentials
                assert hasattr(rate_limit.rate_limit_data, 'points_spent_this_hour')
                
            except GraphQLClientHttpError as e:
                # If we get an auth error with valid creds, that's unexpected
                if e.status_code == 401:
                    pytest.fail("Authentication failed with valid credentials")
                # Other errors are acceptable for this test
                pass

    @pytest.mark.asyncio
    async def test_authentication_error_handling_invalid_token(self):
        """Test authentication error handling with invalid token"""
        # Test with invalid token (should fail)
        invalid_config = {
            "url": "https://www.esologs.com/api/v2/client",
            "headers": {"Authorization": "Bearer invalid_token_12345"}
        }
        
        async with Client(**invalid_config) as client:
            with pytest.raises(GraphQLClientHttpError) as exc_info:
                await client.get_rate_limit_data()
            
            # Should get 401 Unauthorized
            assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_rate_limit_monitoring_example(self, api_client_config):
        """Test the rate limit monitoring pattern"""
        async with Client(**api_client_config) as client:
            
            # Record initial usage
            initial_rate_limit = await client.get_rate_limit_data()
            initial_usage = initial_rate_limit.rate_limit_data.points_spent_this_hour
            
            # Make a request that consumes points
            abilities = await client.get_abilities(limit=10)
            assert len(abilities.game_data.abilities.data) > 0
            
            # Check usage increased
            current_rate_limit = await client.get_rate_limit_data()
            current_usage = current_rate_limit.rate_limit_data.points_spent_this_hour
            
            # Should have consumed some points
            assert current_usage >= initial_usage
            points_consumed = current_usage - initial_usage
            assert points_consumed > 0
            
            # Validate remaining calculation
            remaining = 18000 - current_usage
            assert remaining >= 0

    @pytest.mark.asyncio
    async def test_graphql_error_handling_example(self, api_client_config):
        """Test GraphQL error handling patterns"""
        async with Client(**api_client_config) as client:
            
            # Test GraphQL validation error with limit too high
            with pytest.raises((GraphQLClientGraphQLMultiError, GraphQLClientGraphQLError)):
                await client.get_abilities(limit=200)  # Should exceed max limit

    @pytest.mark.asyncio
    async def test_network_error_handling_patterns(self, api_client_config):
        """Test network error handling concepts (using valid endpoint)"""
        # We can't easily test actual network failures without changing endpoints
        # but we can test the pattern with valid requests
        async with Client(**api_client_config) as client:
            
            try:
                rate_limit = await client.get_rate_limit_data()
                assert hasattr(rate_limit.rate_limit_data, 'points_spent_this_hour')
                
            except httpx.TimeoutException:
                pytest.skip("Network timeout during test")
                
            except httpx.ConnectError:
                pytest.skip("Network connection error during test")
                
            except GraphQLClientHttpError as e:
                # Server errors (5xx) might happen
                if e.status_code >= 500:
                    pytest.skip(f"Server error {e.status_code} during test")
                else:
                    # Re-raise client errors
                    raise

    @pytest.mark.asyncio
    async def test_rate_limit_monitor_class_pattern(self, api_client_config):
        """Test the RateLimitMonitor class pattern"""
        async with Client(**api_client_config) as client:
            
            # Simplified version of the RateLimitMonitor pattern
            # Record initial usage
            initial_rate_limit = await client.get_rate_limit_data()
            initial_usage = initial_rate_limit.rate_limit_data.points_spent_this_hour
            
            # Perform operations with monitoring
            abilities = await client.get_abilities(limit=10)
            
            # Check usage after operation
            current_rate_limit = await client.get_rate_limit_data()
            current_usage = current_rate_limit.rate_limit_data.points_spent_this_hour
            
            # Validate monitoring functionality
            consumed = current_usage - initial_usage
            remaining = 18000 - current_usage
            
            assert consumed >= 0
            assert remaining >= 0
            assert len(abilities.game_data.abilities.data) > 0

    @pytest.mark.asyncio
    async def test_robust_api_call_pattern(self, api_client_config):
        """Test the robust API call pattern with retry logic"""
        async with Client(**api_client_config) as client:
            
            # Simplified version that tests the pattern without forcing failures
            async def test_operation():
                return await client.get_rate_limit_data()
            
            # Test successful operation (no retries needed)
            result = await test_operation()
            assert hasattr(result.rate_limit_data, 'points_spent_this_hour')
            
            # Test the pattern works with normal operations
            abilities = await client.get_abilities(limit=10)
            assert len(abilities.game_data.abilities.data) > 0

    @pytest.mark.asyncio 
    async def test_session_management_pattern(self, api_client_config):
        """Test the session management pattern"""
        # Simplified version of the APISession pattern
        async with Client(**api_client_config) as client:
            
            # Validate session with a health check
            rate_limit = await client.get_rate_limit_data()
            is_healthy = hasattr(rate_limit.rate_limit_data, 'points_spent_this_hour')
            assert is_healthy
            
            # Perform operations in the session
            abilities = await client.get_abilities(limit=5)
            assert len(abilities.game_data.abilities.data) > 0
            
            # Another health check
            rate_limit2 = await client.get_rate_limit_data()
            assert hasattr(rate_limit2.rate_limit_data, 'points_spent_this_hour')

    @pytest.mark.asyncio
    async def test_paced_requests_pattern(self, api_client_config):
        """Test the paced requests pattern for rate limit management"""
        async with Client(**api_client_config) as client:
            
            # Test paced requests with small delays
            request_count = 3
            results = []
            
            for i in range(request_count):
                # Get rate limit data (low-cost operation)
                rate_limit = await client.get_rate_limit_data()
                results.append(rate_limit.rate_limit_data.points_spent_this_hour)
                
                # Small delay between requests (shortened for testing)
                if i < request_count - 1:
                    await asyncio.sleep(0.1)  # 100ms for testing
            
            # Validate all requests succeeded
            assert len(results) == request_count
            assert all(isinstance(usage, (int, float)) for usage in results)
            
            # Usage should generally increase (or stay same for cached results)
            assert results[-1] >= results[0]

    @pytest.mark.asyncio
    async def test_point_consumption_monitoring(self, api_client_config):
        """Test monitoring different endpoint point consumption"""
        async with Client(**api_client_config) as client:
            
            # Get baseline
            baseline = await client.get_rate_limit_data()
            baseline_usage = baseline.rate_limit_data.points_spent_this_hour
            
            # Test simple endpoint (should be low cost)
            classes = await client.get_classes()
            after_classes = await client.get_rate_limit_data()
            classes_cost = after_classes.rate_limit_data.points_spent_this_hour - baseline_usage
            
            # Test paginated endpoint (might be higher cost)
            abilities = await client.get_abilities(limit=10)
            after_abilities = await client.get_rate_limit_data()
            abilities_cost = after_abilities.rate_limit_data.points_spent_this_hour - after_classes.rate_limit_data.points_spent_this_hour
            
            # Validate operations worked
            assert len(classes.game_data.classes) > 0
            assert len(abilities.game_data.abilities.data) > 0
            
            # Validate point consumption tracking
            assert classes_cost >= 0
            assert abilities_cost >= 0
            
            # Total consumption should be positive
            total_consumed = after_abilities.rate_limit_data.points_spent_this_hour - baseline_usage
            assert total_consumed > 0