"""Request payload validation helpers."""

from app.errors import ValidationError


def require_json_object(payload):
    """Ensure the request body is a JSON object."""
    if not isinstance(payload, dict):
        raise ValidationError("Request body must be a JSON object")
    return payload


def require_string(payload, field):
    """Return a stripped, non-empty string from ``payload``."""
    value = payload.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"'{field}' is required")
    return value.strip()


def require_integer(payload, field, minimum=None):
    """Return an integer from ``payload``, rejecting booleans and floats."""
    value = payload.get(field)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"'{field}' must be an integer")
    if minimum is not None and value < minimum:
        if minimum == 0:
            raise ValidationError(f"'{field}' must be a non-negative integer")
        if minimum == 1:
            raise ValidationError(f"'{field}' must be a positive integer")
        raise ValidationError(f"'{field}' must be greater than or equal to {minimum}")
    return value


def validate_item_payload(payload):
    """Validate the POST /items body and return ``(name, total_stock)``."""
    require_json_object(payload)
    name = require_string(payload, "name")
    total_stock = require_integer(payload, "total_stock", minimum=0)
    return name, total_stock


def validate_loan_payload(payload):
    """Validate the POST /loans body and return its fields."""
    require_json_object(payload)
    student_id = require_string(payload, "student_id")
    item_id = require_integer(payload, "item_id", minimum=1)
    quantity = require_integer(payload, "quantity", minimum=1)
    return student_id, item_id, quantity
