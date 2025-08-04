"""
User data related methods for ESO Logs API client.

This mixin provides access to user-specific data that requires OAuth2 user authentication.
These methods require the "view-user-profile" scope and must be used with user tokens.
"""

from typing import TYPE_CHECKING, Any, Dict, Optional, Protocol

from esologs._generated.get_current_user import GetCurrentUser
from esologs._generated.get_user_by_id import GetUserById
from esologs._generated.get_user_data import GetUserData
from esologs.method_factory import create_complex_method, create_no_params_getter

if TYPE_CHECKING:
    import httpx


class ClientProtocol(Protocol):
    """Protocol for ESO Logs client methods needed by user data operations."""

    async def execute(
        self,
        query: str,
        operation_name: Optional[str] = None,
        variables: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> "httpx.Response":
        """Execute a GraphQL query."""
        ...

    def get_data(self, response: "httpx.Response") -> Dict[str, Any]:
        """Extract data from GraphQL response."""
        ...


class UserMixin:
    """Mixin class for user data-related operations.

    Note: All methods in this mixin require OAuth2 user authentication with
    the "view-user-profile" scope. They will not work with client credentials.

    Additionally, the currentUser query requires using the /api/v2/user endpoint
    instead of the standard /api/v2/client endpoint.
    """

    def __init_subclass__(cls, **kwargs: Any):
        """Initialize the subclass with user data methods."""
        super().__init_subclass__(**kwargs)
        cls._register_user_methods()

    @classmethod
    def _register_user_methods(cls) -> None:
        """Register all user data-related methods on the class."""

        # get_user_by_id - use create_complex_method for custom parameter name
        method = create_complex_method(
            operation_name="getUserById",
            return_type=GetUserById,
            required_params={"user_id": int},
            optional_params={},
            param_mapping={"user_id": "userId"},
        )
        cls.get_user_by_id = method  # type: ignore[attr-defined]

        # get_current_user - no params getter (requires user endpoint)
        method = create_no_params_getter(
            operation_name="getCurrentUser",
            return_type=GetCurrentUser,
        )
        cls.get_current_user = method  # type: ignore[attr-defined]

        # get_user_data - no params getter (for testing/validation)
        method = create_no_params_getter(
            operation_name="getUserData",
            return_type=GetUserData,
        )
        cls.get_user_data = method  # type: ignore[attr-defined]

        # Add method docstrings after methods are created
        if hasattr(cls, "get_user_by_id"):
            cls.get_user_by_id.__doc__ = """Get a specific user by their ID.

    Requires OAuth2 user authentication with "view-user-profile" scope.

    Args:
        user_id: The ID of the user to retrieve

    Returns:
        GetUserById: User information including guilds and characters

    Note:
        The guilds and characters fields will only be populated if the
        requesting user has the "view-user-profile" scope.
    """

        if hasattr(cls, "get_current_user"):
            cls.get_current_user.__doc__ = """Get the currently authenticated user.

    Requires OAuth2 user authentication with "view-user-profile" scope.
    This method must be used with the /api/v2/user endpoint.

    Returns:
        GetCurrentUser: Current user information including guilds and characters

    Note:
        This method will not work with client credentials authentication.
        It requires a user access token obtained through the OAuth2
        Authorization Code flow.
    """

        if hasattr(cls, "get_user_data"):
            cls.get_user_data.__doc__ = """Get the userData root object (primarily for testing).

    Requires OAuth2 user authentication.

    Returns:
        GetUserData: The userData root object

    Note:
        This is primarily used for testing the user data API connection.
        For practical use, prefer get_user_by_id or get_current_user.
    """
