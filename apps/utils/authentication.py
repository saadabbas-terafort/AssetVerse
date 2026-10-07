from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.app_settings.models import AppSetting
from apps.users.models import PublicUserToken


class PublicTokenAuthentication(BaseAuthentication):
    keyword = "PublicToken"

    def authenticate(self, request):
        authorization = request.headers.get("Authorization", "")
        parts = authorization.split()
        if not parts or parts[0] != self.keyword:
            return None
        if len(parts) != 2:
            raise AuthenticationFailed("Invalid PublicToken authorization header.")

        app_name = request.headers.get("X-App-Name", "")
        token = PublicUserToken.objects.select_related("user").filter(key=parts[1]).first()
        if token is None:
            raise AuthenticationFailed("Invalid public token.")

        user = token.user
        if not user.is_active:
            raise AuthenticationFailed("Public user is inactive.")
        if not app_name or user.app_name != app_name:
            raise AuthenticationFailed("Public token app does not match X-App-Name.")
        if not AppSetting.objects.filter(slug=app_name, is_active=True).exists():
            raise AuthenticationFailed("Unknown or inactive app name.")

        return user, token

    def authenticate_header(self, request):
        return self.keyword