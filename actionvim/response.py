from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def success_response(data=None, message="Success", status=HTTP_200_OK):
    return Response(
        {"success": True, "message": message, "data": data, "errors": None},
        status=status,
    )


def error_response(
    errors=None, message="Something went wrong", status=HTTP_400_BAD_REQUEST
):
    return Response(
        {
            "success": False,
            "message": message,
            "data": None,
            "errors": errors if errors is not None else {},
        },
        status=status,
    )
