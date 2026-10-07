from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data
    if isinstance(detail, dict) and set(detail) == {"detail"}:
        detail = detail["detail"]
    response.data = {
        "status": response.status_code,
        "data": {},
        "message": detail,
    }
    return response