from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema
from . import views


urlpatterns = [
    path('users/register/', views.UserRegistrationView.as_view(), name='register'),
    path('users/attach-user-to-company/', views.AttachUserToCompanyView.as_view(), name='attach-user-to-company'),

    path('login/',
         extend_schema_view(
             post=extend_schema(tags=['api'], summary='')
         )(TokenObtainPairView.as_view()),
         name='token_obtain_pair'),

    path('token/refresh/',
         extend_schema_view(
             post=extend_schema(tags=['api'], summary='')
         )(TokenRefreshView.as_view()),
         name='token_refresh'),
]