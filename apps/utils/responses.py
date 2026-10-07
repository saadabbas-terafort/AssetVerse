from rest_framework.response import Response


def absolute_file_url(request, file_field):
    if not file_field:
        return None
    url = file_field.url
    if url.startswith(("http://", "https://")):
        return url
    return request.build_absolute_uri(url)


def success_response(data=None, message="Success", status_code=200):
    return Response(
        {
            "status": status_code,
            "data": data if data is not None else {},
            "message": message,
        },
        status=status_code,
    )


def error_response(message, status_code=400, data=None):
    return Response(
        {
            "status": status_code,
            "data": data if data is not None else {},
            "message": message,
        },
        status=status_code,
    )