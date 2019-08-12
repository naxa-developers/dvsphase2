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
from django.urls import path,include
from testing import views
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import SchemaGenerator

schema_view = get_swagger_view(title='DFID API DOCS')

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('<int:pk>',views.product_detail,name='detail'),
    path('admin/', admin.site.urls),
    path('',schema_view),
    path('Hydro',views.ProductViewSet.as_view(),name='Hydro'),
    path('sentry-debug/', trigger_error),
    path('core/', include('core.urls')),
]
