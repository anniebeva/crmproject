from django.urls import path
from .views import SupplierCreateView, SupplierDeleteView, SupplierDetailView, SupplierEditView

urlpatterns = [
    path('create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('<int:pk>/edit/', SupplierEditView.as_view(), name='supplier-edit'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='suppllier-delete')
]