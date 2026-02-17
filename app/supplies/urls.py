from django.urls import path
from .views import SupplyCreateView, SupplyEditView, SupplyDeleteView, SupplyDetailVIew

urlpatterns = [
    path('create/', SupplyCreateView.as_view(), name='supply-create'),
    path('<int:pk>/', SupplyDetailVIew.as_view(), name='supply-detail'),
    path('<int:pk>/edit/', SupplyEditView.as_view(), name='supply-edit'),
    path('<int:pk>/delete/', SupplyDeleteView.as_view(), name='supply-delete'),
]
