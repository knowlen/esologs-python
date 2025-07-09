"""Parameter validation utilities for ESO Logs API client."""

import re
from typing import Any, Optional, Union

from .exceptions import ValidationError


def validate_report_code(code: str) -> None:
    """
    Validate report code format.
    
    Args:
        code: The report code to validate
        
    Raises:
        ValidationError: If the code format is invalid
    """
    if not code:
        raise ValidationError("Report code cannot be empty")
    
    if not isinstance(code, str):
        raise ValidationError("Report code must be a string")
    
    # ESO Logs report codes are typically alphanumeric
    if not re.match(r'^[a-zA-Z0-9]+$', code):
        raise ValidationError("Report code must contain only alphanumeric characters")
    
    if len(code) < 3:
        raise ValidationError("Report code must be at least 3 characters long")


def validate_ability_id(ability_id: Optional[Union[float, int]]) -> None:
    """
    Validate ability ID parameter.
    
    Args:
        ability_id: The ability ID to validate
        
    Raises:
        ValidationError: If the ability ID is invalid
    """
    if ability_id is None:
        return
    
    if not isinstance(ability_id, (int, float)):
        raise ValidationError("Ability ID must be a number")
    
    if ability_id <= 0:
        raise ValidationError("Ability ID must be positive")
    
    # Check if it's a whole number (even if passed as float)
    if isinstance(ability_id, float) and not ability_id.is_integer():
        raise ValidationError("Ability ID should be a whole number")


def validate_time_range(start_time: Optional[float], end_time: Optional[float]) -> None:
    """
    Validate time range parameters.
    
    Args:
        start_time: Start time timestamp
        end_time: End time timestamp
        
    Raises:
        ValidationError: If the time range is invalid
    """
    if start_time is not None and not isinstance(start_time, (int, float)):
        raise ValidationError("Start time must be a number")
    
    if end_time is not None and not isinstance(end_time, (int, float)):
        raise ValidationError("End time must be a number")
    
    if start_time is not None and start_time < 0:
        raise ValidationError("Start time cannot be negative")
    
    if end_time is not None and end_time < 0:
        raise ValidationError("End time cannot be negative")
    
    if start_time is not None and end_time is not None and start_time >= end_time:
        raise ValidationError("Start time must be less than end time")


def validate_positive_integer(value: Optional[int], param_name: str) -> None:
    """
    Validate that a parameter is a positive integer.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        
    Raises:
        ValidationError: If the value is invalid
    """
    if value is None:
        return
    
    if not isinstance(value, int):
        raise ValidationError(f"{param_name} must be an integer")
    
    if value <= 0:
        raise ValidationError(f"{param_name} must be positive")


def validate_limit_parameter(limit: Optional[int]) -> None:
    """
    Validate limit parameter for pagination.
    
    Args:
        limit: The limit value to validate
        
    Raises:
        ValidationError: If the limit is invalid
    """
    if limit is None:
        return
    
    if not isinstance(limit, int):
        raise ValidationError("Limit must be an integer")
    
    if limit <= 0:
        raise ValidationError("Limit must be positive")
    
    if limit > 10000:  # Reasonable upper bound
        raise ValidationError("Limit cannot exceed 10,000")


def validate_fight_ids(fight_ids: Optional[list]) -> None:
    """
    Validate fight IDs parameter.
    
    Args:
        fight_ids: List of fight IDs to validate
        
    Raises:
        ValidationError: If the fight IDs are invalid
    """
    if fight_ids is None:
        return
    
    if not isinstance(fight_ids, list):
        raise ValidationError("Fight IDs must be a list")
    
    for fight_id in fight_ids:
        if fight_id is not None and not isinstance(fight_id, int):
            raise ValidationError("Fight ID must be an integer")
        
        if fight_id is not None and fight_id <= 0:
            raise ValidationError("Fight ID must be positive")


def validate_required_string(value: Any, param_name: str) -> None:
    """
    Validate that a required parameter is a non-empty string.
    
    Args:
        value: The value to validate
        param_name: Name of the parameter for error messages
        
    Raises:
        ValidationError: If the value is invalid
    """
    if value is None:
        raise ValidationError(f"{param_name} is required")
    
    if not isinstance(value, str):
        raise ValidationError(f"{param_name} must be a string")
    
    if not value.strip():
        raise ValidationError(f"{param_name} cannot be empty")