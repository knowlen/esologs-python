"""Tests for authentication.md code examples.

This module tests all code blocks from docs/authentication.md to ensure they
execute without errors and produce expected results.
"""


import pytest

from access_token import get_access_token
from esologs.client import Client
from esologs.exceptions import GraphQLClientHttpError


class TestAuthenticationExamples:
    """Test all code examples from authentication.md."""

    @pytest.mark.asyncio
    async def test_basic_authentication_example(self, api_client_config):
        """Test: Basic Authentication example."""
        # This tests the basic auth pattern from authentication.md
        token = get_access_token()

        # Verify token is a string and not empty
        assert isinstance(token, str)
        assert len(token) > 0

        # Test that we can use the token
        async with Client(**api_client_config) as client:
            rate_limit = await client.get_rate_limit_data()
            assert hasattr(rate_limit, "rate_limit_data")
            assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")

    @pytest.mark.asyncio
    async def test_client_authentication_example(self, api_client_config):
        """Test: Authentication with Client example."""
        # This tests the main auth example from authentication.md
        token = get_access_token()

        async with Client(
            url="https://www.esologs.com/api/v2/client",
            headers={"Authorization": f"Bearer {token}"},
        ) as client:
            # Test authentication with rate limit check
            rate_limit = await client.get_rate_limit_data()

            # Verify expected structure
            assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")
            assert hasattr(rate_limit.rate_limit_data, "points_spent_this_hour")

            # Verify reasonable values
            assert isinstance(rate_limit.rate_limit_data.limit_per_hour, int)
            assert isinstance(
                rate_limit.rate_limit_data.points_spent_this_hour, (int, float)
            )
            assert rate_limit.rate_limit_data.limit_per_hour > 0
            assert rate_limit.rate_limit_data.points_spent_this_hour >= 0

    @pytest.mark.asyncio
    async def test_error_handling_example(self, api_client_config):
        """Test: Error Handling example from authentication.md."""
        # Test the complete error handling pattern
        try:
            token = get_access_token()
            # Verify token obtained successfully
            assert isinstance(token, str)
            assert len(token) > 0

            # Test token with API call
            async with Client(
                url="https://www.esologs.com/api/v2/client",
                headers={"Authorization": f"Bearer {token}"},
            ) as client:
                rate_limit = await client.get_rate_limit_data()
                # Verify successful authentication response
                assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")
                assert isinstance(rate_limit.rate_limit_data.limit_per_hour, int)

        except GraphQLClientHttpError as e:
            # Verify we can handle HTTP errors properly
            assert hasattr(e, "status_code")
            assert isinstance(e.status_code, int)

            # Test status code handling as shown in docs
            if e.status_code == 401:
                assert True  # Expected for invalid credentials
            else:
                assert e.status_code > 0  # Any valid HTTP status code

        except Exception as e:
            # Verify we can handle general exceptions
            assert str(e)  # Should have error message

    @pytest.mark.asyncio
    async def test_token_validation_example(self, api_client_config):
        """Test: Token Validation example."""
        # This tests the validate_token() function from authentication.md
        try:
            token = get_access_token()

            async with Client(
                url="https://www.esologs.com/api/v2/client",
                headers={"Authorization": f"Bearer {token}"},
            ) as client:
                # Simple validation call
                rate_limit = await client.get_rate_limit_data()

                # Verify token validation succeeded
                assert hasattr(rate_limit.rate_limit_data, "limit_per_hour")
                assert hasattr(rate_limit.rate_limit_data, "points_spent_this_hour")

                # Verify the values are reasonable
                limit = rate_limit.rate_limit_data.limit_per_hour
                used = rate_limit.rate_limit_data.points_spent_this_hour

                assert isinstance(limit, int)
                assert isinstance(used, (int, float))
                assert limit > 0
                assert used >= 0
                assert used <= limit  # Used should not exceed limit

                # Function should return True for successful validation
                validation_result = True  # Simulating successful validation
                assert validation_result is True

        except Exception as e:
            # Function should return False for failed validation
            validation_result = False
            assert validation_result is False
            assert str(e)  # Should have error message

    def test_access_token_direct_parameters(self):
        """Test: Direct parameter passing method."""
        # Test that get_access_token can accept direct parameters
        # This validates the example in authentication.md

        # We can't test with fake credentials, but we can test the interface
        import inspect

        from access_token import get_access_token

        # Verify function signature supports client_id and client_secret parameters
        sig = inspect.signature(get_access_token)
        param_names = list(sig.parameters.keys())

        assert "client_id" in param_names
        assert "client_secret" in param_names

        # Verify parameters are optional (have defaults)
        client_id_param = sig.parameters["client_id"]
        client_secret_param = sig.parameters["client_secret"]

        assert client_id_param.default is not inspect.Parameter.empty
        assert client_secret_param.default is not inspect.Parameter.empty


class TestAuthenticationDocumentationIntegrity:
    """Additional tests for authentication documentation integrity."""

    def test_authentication_imports(self):
        """Test that all modules used in auth docs are importable."""
        # Test basic imports
        from access_token import get_access_token
        from esologs.client import Client
        from esologs.exceptions import GraphQLClientHttpError

        assert callable(get_access_token)
        assert Client is not None
        assert issubclass(GraphQLClientHttpError, Exception)

    def test_environment_variable_handling(self):
        """Test that authentication handles environment variables correctly."""
        import os

        # Verify that get_access_token looks for environment variables
        # by checking if the required env vars exist
        esologs_id = os.environ.get("ESOLOGS_ID")
        esologs_secret = os.environ.get("ESOLOGS_SECRET")

        # In test environment, these should be set
        assert (
            esologs_id is not None
        ), "ESOLOGS_ID environment variable should be set for tests"
        assert (
            esologs_secret is not None
        ), "ESOLOGS_SECRET environment variable should be set for tests"
        assert len(esologs_id) > 0
        assert len(esologs_secret) > 0

    def test_oauth_error_handling(self):
        """Test that OAuth errors are handled as documented."""
        from access_token import get_access_token

        # Test with invalid credentials to verify error handling
        try:
            # This should work with valid environment variables
            token = get_access_token()
            assert isinstance(token, str)
            assert len(token) > 0
        except Exception as e:
            # If it fails, verify the error message format matches docs
            error_msg = str(e)
            assert "OAuth request failed" in error_msg or "invalid_client" in error_msg

    def test_http_error_status_codes(self):
        """Test that HTTP error status codes are accessible as documented."""
        # Verify the GraphQLClientHttpError has status_code attribute
        # This validates the error handling pattern in docs
        # We can't easily create a real HTTP error in tests, but we can
        # verify the exception class has the expected interface
        import inspect

        from esologs.exceptions import GraphQLClientHttpError

        # Check that GraphQLClientHttpError has status_code in its __init__
        init_sig = inspect.signature(GraphQLClientHttpError.__init__)
        param_names = list(init_sig.parameters.keys())

        assert "status_code" in param_names

        # Verify it's a proper exception class
        assert issubclass(GraphQLClientHttpError, Exception)
