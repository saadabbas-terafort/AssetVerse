import uuid

from django.db import transaction
from rest_framework.views import APIView

from apps.app_settings.models import AppSetting
from apps.users.models import PublicUser, PublicUserToken
from apps.utils.responses import error_response, success_response


class DeviceAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        app_name = request.headers.get("X-App-Name") or request.META.get("HTTP_X_APP_NAME")
        if not app_name:
            return error_response("Missing X-App-Name header.", status_code=400)

        app = AppSetting.objects.filter(slug=app_name, is_active=True).first()
        if not app:
            return error_response("Unknown or inactive app name.", status_code=403)

        device_id = (request.data or {}).get("device_id")
        if not device_id or not str(device_id).strip():
            return error_response("device_id is required.", status_code=400)

        device_id = str(device_id).strip()

        with transaction.atomic():
            public_user, created = PublicUser.objects.get_or_create(
                device_id=device_id,
                app_name=app_name,
                defaults={"is_active": True},
            )

            if not public_user.is_active:
                return error_response("This device user is inactive.", status_code=403)

            if public_user.app_name != app_name:
                return error_response("Token app does not match the header app.", status_code=403)

            PublicUserToken.objects.filter(user=public_user).delete()
            token = PublicUserToken.objects.create(
                key=uuid.uuid4().hex,
                user=public_user,
            )

        payload = {
            "token": token.key,
            "user": {
                "id": str(public_user.id),
                "device_id": public_user.device_id,
                "app_name": public_user.app_name,
                "is_active": public_user.is_active,
            },
        }
        message = "User registered successfully" if created else "User logged in successfully"
        return success_response(payload, message=message, status_code=200)
