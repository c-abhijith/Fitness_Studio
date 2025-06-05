from rest_framework.response import Response
from rest_framework import status

def handle_internal_server_error(message: str, error: Exception):
    return Response(
        {
            "status": 500,
            "message": message,
            "error": str(error)
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

def handle_Bad_request(message: str):
    return Response(
        {
            "status": 400,
            "message": "Bad Request",
            "error": message
        },
        status=status.HTTP_400_BAD_REQUEST
    )

def handle_not_found(message: str):
    return Response(
        {
            "status": 404,
            "message": "Bad Request",
            "error": message
        },
        status=status.HTTP_404_NOT_FOUND
    )

def handle_forbidden(message: str):
    return Response(
        {
            "status": 403,
            "message": "Forbidden",
            "error": message
        },
        status=status.HTTP_403_FORBIDDEN
    )