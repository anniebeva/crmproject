from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authenticate.urls')),
    path('api/companies/', include('companies.urls')),
    path('api/storage/', include('storage.urls')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/supplies/', include('supplies.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
