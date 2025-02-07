from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Swagger and Redoc documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Yuhu Challenge Backend API",
        default_version="v1",
        description="This is the API documentation for Yuhu Challenge Backend",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hugazo98g@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger<format>/", schema_view.with_ui(cache_timeout=0), name="schema-json"),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("", include("tasks.urls")),
                path("", include("userauths.urls")),
            ]
        ),
    ),
]
