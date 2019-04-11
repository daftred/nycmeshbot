"""nycmeshbot URL Configuration

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
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="NYC Mesh API",
        default_version='v1',
        description="API for various Mesh related properties",
        terms_of_service="https://nycmesh.net",
        contact=openapi.Contact(email="logan@nycmesh.net"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    validators=['ssv'],
    permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('acuity/', include('acuity.urls'), name="acuity-base"),
    re_path(r'^api/docs/$', schema_view.with_ui('swagger'), name='api_docs'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc'), name='api_redocs'),
    re_path(r'^api/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(), name='schema_swagger')
]
