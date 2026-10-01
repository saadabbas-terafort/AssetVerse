from rest_framework.response import Response


def success_response(data, message="Successfully Retrive"):
    return Response(
        {
            "status": 200,
            "data": data,
            "massage": message,
        }
    )