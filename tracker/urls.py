from django.contrib import admin
from django.urls import path, include
from .settings.base import DEBUG
from decouple import config

handler404 = "tracker.apps.core.views.custom_page_not_found_view"
handler500 = "tracker.apps.core.views.custom_error_view"
handler403 = "tracker.apps.core.views.custom_permission_denied_view"
handler400 = "tracker.apps.core.views.custom_bad_request_view"

urlpatterns = [
    path("accounts/", include("tracker.apps.accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("tracker.apps.core.urls")),
    path(config("ADMIN_URL") + "/", admin.site.urls),
]

if DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from .settings.base import MEDIA_URL, MEDIA_ROOT

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
