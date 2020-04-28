"""dvs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.contrib.auth import views as auth_views





schema_view = get_schema_view(
    openapi.Info(
        title="Dvs Api Doc",
        default_version='v1',
    ),
)

urlpatterns = [

    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/core/', include('core.urls')),
    path('api/v1/covid/', include('covid.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('federal/', include('federal.urls')),

    path('', auth_views.LoginView.as_view(), name='login'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # import debug_toolbar
    #
    # urlpatterns = [
    #                   path('__debug__/', include(debug_toolbar.urls)),
    #
    #                   # For django versions before 2.0:
    #                   # url(r'^__debug__/', include(debug_toolbar.urls)),
    #
    #               ] + urlpatterns
