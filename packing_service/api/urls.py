from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import OrdersView, PackageView

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="API documentation",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('v1/orders/', OrdersView.as_view(), name='orders'),
    path('v1/packaging/<str:orderkey>/', PackageView.as_view(), name='packaging'),
    path('v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
]
