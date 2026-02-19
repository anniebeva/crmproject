from django.urls import path
from .views import CompanyCreateView, CompanyDeleteView, CompanyDetailView, CompanyEditView

urlpatterns = [
    path('create/', CompanyCreateView.as_view(), name='company-create'),
    path('<int:pk>/', CompanyDetailView.as_view(), name='company-detail'),
    path('<int:pk>/edit/', CompanyEditView.as_view(), name='company-edit'),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete')
]