"""Unit tests for parameter validation functions."""

import pytest

from esologs.validators import (
    ValidationError,
    validate_ability_id,
    validate_fight_ids,
    validate_limit_parameter,
    validate_positive_integer,
    validate_report_code,
    validate_required_string,
    validate_time_range,
)


class TestValidateReportCode:
    """Test report code validation."""

    def test_valid_codes(self):
        """Test valid report codes."""
        validate_report_code("ABC123")
        validate_report_code("TestReport")
        validate_report_code("abc123def")

    def test_empty_code(self):
        """Test empty report code raises error."""
        with pytest.raises(ValidationError, match="Report code cannot be empty"):
            validate_report_code("")

    def test_non_string_code(self):
        """Test non-string report code raises error."""
        with pytest.raises(ValidationError, match="Report code must be a string"):
            validate_report_code(123)

    def test_invalid_characters(self):
        """Test report code with invalid characters."""
        with pytest.raises(
            ValidationError, match="must contain only alphanumeric characters"
        ):
            validate_report_code("ABC-123")

    def test_too_short(self):
        """Test report code that's too short."""
        with pytest.raises(ValidationError, match="must be at least 3 characters long"):
            validate_report_code("AB")


class TestValidateAbilityId:
    """Test ability ID validation."""

    def test_valid_ids(self):
        """Test valid ability IDs."""
        validate_ability_id(None)  # None is valid
        validate_ability_id(123)  # int
        validate_ability_id(123.0)  # float that's a whole number

    def test_invalid_type(self):
        """Test invalid ability ID type."""
        with pytest.raises(ValidationError, match="Ability ID must be a number"):
            validate_ability_id("123")

    def test_negative_id(self):
        """Test negative ability ID."""
        with pytest.raises(ValidationError, match="Ability ID must be positive"):
            validate_ability_id(-1)

    def test_float_non_integer(self):
        """Test float that's not a whole number."""
        with pytest.raises(
            ValidationError, match="Ability ID should be a whole number"
        ):
            validate_ability_id(123.5)


class TestValidateTimeRange:
    """Test time range validation."""

    def test_valid_ranges(self):
        """Test valid time ranges."""
        validate_time_range(None, None)
        validate_time_range(0, 100)
        validate_time_range(0.0, 100.5)

    def test_invalid_start_type(self):
        """Test invalid start time type."""
        with pytest.raises(ValidationError, match="Start time must be a number"):
            validate_time_range("0", 100)

    def test_invalid_end_type(self):
        """Test invalid end time type."""
        with pytest.raises(ValidationError, match="End time must be a number"):
            validate_time_range(0, "100")

    def test_negative_start(self):
        """Test negative start time."""
        with pytest.raises(ValidationError, match="Start time cannot be negative"):
            validate_time_range(-1, 100)

    def test_negative_end(self):
        """Test negative end time."""
        with pytest.raises(ValidationError, match="End time cannot be negative"):
            validate_time_range(0, -1)

    def test_start_after_end(self):
        """Test start time after end time."""
        with pytest.raises(
            ValidationError, match="Start time must be less than end time"
        ):
            validate_time_range(100, 50)


class TestValidatePositiveInteger:
    """Test positive integer validation."""

    def test_valid_values(self):
        """Test valid positive integers."""
        validate_positive_integer(None, "test_param")
        validate_positive_integer(1, "test_param")
        validate_positive_integer(100, "test_param")

    def test_non_integer(self):
        """Test non-integer value."""
        with pytest.raises(ValidationError, match="test_param must be an integer"):
            validate_positive_integer(1.5, "test_param")

    def test_zero_or_negative(self):
        """Test zero or negative integer."""
        with pytest.raises(ValidationError, match="test_param must be positive"):
            validate_positive_integer(0, "test_param")

        with pytest.raises(ValidationError, match="test_param must be positive"):
            validate_positive_integer(-1, "test_param")


class TestValidateLimitParameter:
    """Test limit parameter validation."""

    def test_valid_limits(self):
        """Test valid limit values."""
        validate_limit_parameter(None)
        validate_limit_parameter(1)
        validate_limit_parameter(100)
        validate_limit_parameter(10000)

    def test_non_integer(self):
        """Test non-integer limit."""
        with pytest.raises(ValidationError, match="Limit must be an integer"):
            validate_limit_parameter(1.5)

    def test_zero_or_negative(self):
        """Test zero or negative limit."""
        with pytest.raises(ValidationError, match="Limit must be positive"):
            validate_limit_parameter(0)

    def test_too_large(self):
        """Test limit that's too large."""
        with pytest.raises(ValidationError, match="Limit cannot exceed 10,000"):
            validate_limit_parameter(10001)


class TestValidateFightIds:
    """Test fight IDs validation."""

    def test_valid_ids(self):
        """Test valid fight ID lists."""
        validate_fight_ids(None)
        validate_fight_ids([])
        validate_fight_ids([1, 2, 3])
        validate_fight_ids([None, 1, None])  # None values allowed

    def test_non_list(self):
        """Test non-list fight IDs."""
        with pytest.raises(ValidationError, match="Fight IDs must be a list"):
            validate_fight_ids(123)

    def test_invalid_id_type(self):
        """Test invalid fight ID type."""
        with pytest.raises(ValidationError, match="Fight ID must be an integer"):
            validate_fight_ids([1, "2", 3])

    def test_negative_id(self):
        """Test negative fight ID."""
        with pytest.raises(ValidationError, match="Fight ID must be positive"):
            validate_fight_ids([1, -2, 3])


class TestValidateRequiredString:
    """Test required string validation."""

    def test_valid_strings(self):
        """Test valid required strings."""
        validate_required_string("test", "param")
        validate_required_string("  test  ", "param")  # whitespace is stripped

    def test_none_value(self):
        """Test None value for required string."""
        with pytest.raises(ValidationError, match="param is required"):
            validate_required_string(None, "param")

    def test_non_string(self):
        """Test non-string value."""
        with pytest.raises(ValidationError, match="param must be a string"):
            validate_required_string(123, "param")

    def test_empty_string(self):
        """Test empty string after stripping."""
        with pytest.raises(ValidationError, match="param cannot be empty"):
            validate_required_string("", "param")

        with pytest.raises(ValidationError, match="param cannot be empty"):
            validate_required_string("   ", "param")
