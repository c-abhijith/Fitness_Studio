from rest_framework.response import Response
from rest_framework import status
from typing import Any, Optional

def handle_ok(message: str, data: Optional[Any] = None,page: Optional[Any] = None,paginator: Optional[Any] = None):
    response = {
        "status": 200,
        "message": message
    }
    if data is not None:
        response["data"] = data
        response["count"]=int(len(data))
        response["page"]=int(page)
        response["pages"]=paginator.num_pages

    return Response(response, status=status.HTTP_200_OK)

def handle_create(message: str,):
    response = {
        "status": 201,
        "message": f"{message} created successfully"
    }

    return Response(response, status=status.HTTP_201_CREATED)