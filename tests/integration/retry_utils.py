"""Retry utilities for integration tests to handle transient failures."""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Tuple, Type, Union

import httpx

logger = logging.getLogger(__name__)


def retry_on_exceptions(
    exceptions: Union[Type[Exception], Tuple[Type[Exception], ...]] = (
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.ConnectError,
        httpx.NetworkError,
    ),
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    max_delay: float = 30.0,
) -> Callable:
    """
    Decorator to retry tests on specific exceptions.

    Args:
        exceptions: Exception types to retry on
        max_attempts: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay between retries
        max_delay: Maximum delay between retries in seconds

    Returns:
        Decorated function that retries on specified exceptions
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Async wrapper for retry logic."""
            last_exception = None
            delay = initial_delay

            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed with "
                            f"{type(e).__name__}: {e}"
                        )
                        logger.info(f"Retrying in {delay} seconds...")
                        await asyncio.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed. "
                            f"Last error: {type(e).__name__}: {e}"
                        )

            # If we get here, all attempts failed
            if last_exception:
                raise last_exception
            return None

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            """Sync wrapper for retry logic."""
            last_exception = None
            delay = initial_delay

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed with "
                            f"{type(e).__name__}: {e}"
                        )
                        logger.info(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay = min(delay * backoff_factor, max_delay)
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed. "
                            f"Last error: {type(e).__name__}: {e}"
                        )

            # If we get here, all attempts failed
            if last_exception:
                raise last_exception
            return None

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Convenience decorator with default settings for integration tests
retry_integration_test = retry_on_exceptions(
    exceptions=(
        httpx.ConnectTimeout,
        httpx.ReadTimeout,
        httpx.ConnectError,
        httpx.NetworkError,
        httpx.HTTPStatusError,
    ),
    max_attempts=3,
    initial_delay=2.0,
    backoff_factor=2.0,
    max_delay=10.0,
)


class RetryClient:
    """
    Wrapper for ESO Logs client that adds retry logic to all API calls.
    """

    def __init__(self, client: Any, **retry_kwargs: Any):
        """
        Initialize retry client wrapper.

        Args:
            client: The ESO Logs client instance
            **retry_kwargs: Keyword arguments for retry_on_exceptions decorator
        """
        self._client = client
        self._retry_kwargs = retry_kwargs or {
            "max_attempts": 3,
            "initial_delay": 1.0,
            "backoff_factor": 2.0,
        }

    def __getattr__(self, name: str) -> Any:
        """
        Wrap client methods with retry logic.

        Args:
            name: Attribute name

        Returns:
            Wrapped method or original attribute
        """
        attr = getattr(self._client, name)

        # If it's a callable method, wrap it with retry logic
        if callable(attr):
            return retry_on_exceptions(**self._retry_kwargs)(attr)

        return attr

    async def __aenter__(self) -> "RetryClient":
        """Async context manager entry."""
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self._client.__aexit__(*args)
