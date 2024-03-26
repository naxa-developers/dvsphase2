from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.contrib.auth import views as auth_views
from drf_yasg.generators import OpenAPISchemaGenerator
import debug_toolbar


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", "https"]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="Dvs Api Doc",
        default_version="v1",
    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/core/", include("core.urls")),
    path("api/v1/covid/", include("covid.urls")),
    path("dashboard/", include("dashboard.urls.urls")),
    path("api/v2/dashboard/", include("dashboard.urls.dashboard_urls")),
    path("federal/", include("federal.urls")),
    path("api/v1/about_us/", include("about_us.urls")),
    path("", auth_views.LoginView.as_view(), name="login"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path(
            "api/docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]
