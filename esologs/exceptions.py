from typing import Any, Dict, List, Optional, Union

import httpx


class GraphQLClientError(Exception):
    """Base exception."""


class GraphQLClientHttpError(GraphQLClientError):
    def __init__(self, status_code: int, response: httpx.Response) -> None:
        self.status_code = status_code
        self.response = response

    def __str__(self) -> str:
        return f"HTTP status code: {self.status_code}"


class GraphQLClientInvalidResponseError(GraphQLClientError):
    def __init__(self, response: httpx.Response) -> None:
        self.response = response

    def __str__(self) -> str:
        return "Invalid response format."


class GraphQLClientGraphQLError(GraphQLClientError):
    def __init__(
        self,
        message: str,
        locations: Optional[List[Dict[str, int]]] = None,
        path: Optional[List[str]] = None,
        extensions: Optional[Dict[str, object]] = None,
        orginal: Optional[Dict[str, object]] = None,
    ):
        self.message = message
        self.locations = locations
        self.path = path
        self.extensions = extensions
        self.orginal = orginal

    def __str__(self) -> str:
        return self.message

    @classmethod
    def from_dict(cls, error: Dict[str, Any]) -> "GraphQLClientGraphQLError":
        return cls(
            message=error["message"],
            locations=error.get("locations"),
            path=error.get("path"),
            extensions=error.get("extensions"),
            orginal=error,
        )


class GraphQLClientGraphQLMultiError(GraphQLClientError):
    def __init__(
        self,
        errors: List[GraphQLClientGraphQLError],
        data: Optional[Dict[str, Any]] = None,
    ):
        self.errors = errors
        self.data = data

    def __str__(self) -> str:
        return "; ".join(str(e) for e in self.errors)

    @classmethod
    def from_errors_dicts(
        cls, errors_dicts: List[Dict[str, Any]], data: Optional[Dict[str, Any]] = None
    ) -> "GraphQLClientGraphQLMultiError":
        return cls(
            errors=[GraphQLClientGraphQLError.from_dict(e) for e in errors_dicts],
            data=data,
        )


class GraphQLClientInvalidMessageFormat(GraphQLClientError):
    def __init__(self, message: Union[str, bytes]) -> None:
        self.message = message

    def __str__(self) -> str:
        return "Invalid message format."


# ESO Logs specific exceptions
class ESOLogsError(GraphQLClientError):
    """Base exception for ESO Logs specific errors."""
    pass


class ReportNotFoundError(ESOLogsError):
    """Raised when a report code doesn't exist."""
    
    def __init__(self, code: str, message: str = None):
        self.code = code
        self.message = message or f"Report '{code}' not found"
        super().__init__(self.message)


class CharacterNotFoundError(ESOLogsError):
    """Raised when a character ID doesn't exist."""
    
    def __init__(self, character_id: int, message: str = None):
        self.character_id = character_id
        self.message = message or f"Character ID {character_id} not found"
        super().__init__(self.message)


class GuildNotFoundError(ESOLogsError):
    """Raised when a guild ID doesn't exist."""
    
    def __init__(self, guild_id: int, message: str = None):
        self.guild_id = guild_id
        self.message = message or f"Guild ID {guild_id} not found"
        super().__init__(self.message)


class AuthenticationError(ESOLogsError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        self.message = message
        super().__init__(self.message)


class RateLimitError(ESOLogsError):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        self.message = message
        self.retry_after = retry_after
        super().__init__(self.message)


class ValidationError(ESOLogsError):
    """Raised when parameter validation fails."""
    
    def __init__(self, message: str, parameter: str = None):
        self.message = message
        self.parameter = parameter
        super().__init__(self.message)


class GraphQLQueryError(ESOLogsError):
    """Raised when GraphQL query fails with additional context."""
    
    def __init__(self, message: str, query: str = None, variables: Dict[str, Any] = None, 
                 operation_name: str = None):
        self.message = message
        self.query = query
        self.variables = variables
        self.operation_name = operation_name
        super().__init__(self.message)
    
    def __str__(self) -> str:
        context = []
        if self.operation_name:
            context.append(f"Operation: {self.operation_name}")
        if self.variables:
            context.append(f"Variables: {self.variables}")
        
        if context:
            return f"{self.message} ({'; '.join(context)})"
        return self.message
