from django.urls import path, re_path
from . import views
from rest_framework.authtoken import views as rest_auth_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Kilola API",
        default_version='v1',
        description="This is an auto generated documentation for the API",
        contact=openapi.Contact(email="hi@menas.pro")
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('login', rest_auth_views.obtain_auth_token),
    path('user', views.UserAPIView.as_view(), name='User API'),
    path('register', views.SignUpView.as_view(), name='SignUp API'),
    path('user/farm', views.UserFarmView.as_view(), name='SignUp API'),
    path(
        'activate',
        views.ConfirmEmailView.as_view(),
        name='Account Activation API'
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui(
            'swagger',
            cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui(
            'redoc',
            cache_timeout=0
        ),
        name='schema-redoc'
    ),
]
