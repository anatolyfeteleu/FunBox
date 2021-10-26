from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

api_schema_view = get_schema_view(
    openapi.Info(title='FunBox API', default_version='1.0'),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    re_path(route=r'^docs(?P<format>\.json|\.yaml)$',
            view=api_schema_view.without_ui(cache_timeout=0),  # NOQA
            name='schema-json'),
    path(route='docs/',
         view=api_schema_view.with_ui('swagger', cache_timeout=10),  # NOQA
         name='swagger'),
    path(route='redocs/',
         view=api_schema_view.with_ui('redoc', cache_timeout=0),  # NOQA
         name='schema-redoc')
    ]
