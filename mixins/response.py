from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

PAGINATOR = {
    "count": 0,
    "next": '',
    "previous": ''
}


def api_response(success=True, message="", data=None, pagination=None, errors=None, status=200):
    """
    Standardized API response method.
    :param success: Boolean indicating success or failure
    :param message: Message to describe the response
    :param data: Data to be returned in the response
    :param pagination: Pagination details (if applicable)
    :param errors: List of errors (if any)
    :param status: HTTP status code
    :return: DRF Response object
    """
    if errors is not None:
        errors = extract_validation_errors(errors)

    if pagination:
        pagination = format_pagination(pagination)

    return Response(
        {
            "success": success,
            "message": message,
            "response": {
                "data": data or [],
                "pagination": pagination or {}
            },
            "errors": errors or []
        },
        status=status
    )


def extract_validation_errors(exc):
    """
    Extract key-value pairs from DRF ValidationError.
    :param exc: ValidationError instance
    :return: List of key-value pairs representing the errors
    """
    if not isinstance(exc, ValidationError):
        return []

    errors = {}

    def flatten_errors(error_dict, parent_key=""):
        """
        Recursive helper function to flatten nested error dictionaries.
        :param error_dict: The error dictionary
        :param parent_key: The parent key to handle nested fields
        """
        for key, value in error_dict.items():
            # Build the full key path for nested fields
            full_key = f"{parent_key}.{key}" if parent_key else key

            if isinstance(value, list):  # Field errors
                for v in value:
                    errors[full_key] = v
            elif isinstance(value, dict):  # Nested field errors
                flatten_errors(value, full_key)

    if isinstance(exc.detail, str):  # Single non-field error as a string
        errors['detail'] = exc.detail
    elif isinstance(exc.detail, dict):
        flatten_errors(exc.detail)
    elif isinstance(exc.detail, list):  # Non-field errors as a list
        for message in exc.detail:
            errors['detail'] = message
    return errors


def format_pagination(data):
    if isinstance(data, dict):
        PAGINATOR['count'] = data.get('count')
        PAGINATOR['next'] = data.get('next')
        PAGINATOR['previous'] = data.get('previous')

    return PAGINATOR
