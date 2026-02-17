from django.utils.translation import gettext as _
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


class ServiceUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Services not available')


class MovedTemporarilyError(Exception):
    message = 'Moved Temporarily'


class NotFoundError(Exception):
    message = 'Not Found'


class GoneError(Exception):
    message = 'Content Gone'


class MovedPermanentlyError(Exception):
    message = 'Moved Permanently'


def custom_exception_handler(exc, context):
    '''
    Custom exception handler that converts all errors into a standard format:
    {
        "message": [<error messages>]
    }
    '''
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, DjangoValidationError):
            return Response(
                {'message': exc.messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'message': [str(exc)]},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    error_messages = []

    if isinstance(exc, DRFValidationError):
        if isinstance(response.data, dict):
            # Handle dictionary of errors
            for field, errors in response.data.items():
                if isinstance(errors, list):
                    # Convert ErrorDetail objects to strings
                    error_messages.extend([str(error) for error in errors])
                elif isinstance(errors, dict):
                    # Handle nested dictionary errors
                    error_messages.extend(flatten_nested_errors(errors))
                elif isinstance(errors, str):
                    error_messages.append(errors)
                else:
                    error_messages.append(str(errors))
        elif isinstance(response.data, list):
            # Handle list of errors
            error_messages.extend([str(error) for error in response.data])
        else:
            # Handle string or other type of error
            error_messages.append(str(response.data))
    else:
        # Handle non-validation errors
        if isinstance(response.data, dict) and 'detail' in response.data:
            error_messages.append(str(response.data['detail']))
        else:
            error_messages.append(str(response.data))

    response.data = {'message': error_messages}
    return response


def flatten_nested_errors(errors_dict):
    """
    Recursively flatten nested error dictionaries into a list of error messages.
    """
    messages = []
    for key, value in errors_dict.items():
        if isinstance(value, list):
            messages.extend([str(error) for error in value])
        elif isinstance(value, dict):
            messages.extend(flatten_nested_errors(value))
        else:
            messages.append(str(value))
    return messages
