from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseNotFound, JsonResponse
from django.urls import include, path


def health_check(request):
    return JsonResponse({"status": 200, "data": {}, "message": "Success"}, status=200)


def api_not_found(request, exception):
    if request.path.startswith("/api/"):
        return JsonResponse(
            {"status": 404, "data": {}, "message": "Not found."},
            status=404,
        )
    return HttpResponseNotFound("Not found.")


urlpatterns = [
    path("health/", health_check, name="health"),
    path("admin/", admin.site.urls),
    path("", include("apps.users.urls")),
    path("", include("apps.lookup.urls")),
    path("", include("apps.category.urls")),
    path("", include("apps.home_assets.urls")),
    path("", include("apps.stickers.urls")),
    path("", include("apps.effects.urls")),
    path("", include("apps.slides.urls")),
    path("", include("apps.fonts.urls")),
    path("silk/", include("silk.urls")),
]

handler404 = "main.urls.api_not_found"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
