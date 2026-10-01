from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path, re_path


def health_check(request):
	return JsonResponse({"status": "ok"})


urlpatterns = [
	re_path(r"^$", health_check, name="health-check"),
	path("health/", health_check, name="health"),
	path("admin/", admin.site.urls),
	path("", include("apps.category.urls")),
	path("", include("apps.home_assets.urls")),
	path("", include("apps.stickers.urls")),
	path("", include("apps.effects.urls")),
	path("", include("apps.slides.urls")),
	path("", include("apps.fonts.urls")),
	path("silk/", include("silk.urls")),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)