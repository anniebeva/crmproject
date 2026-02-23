from django.urls import path
from.views import ProductCreateView, ProductDetailView, ProductEditView, ProductDeleteView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/edit/', ProductEditView.as_view(), name='product-edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete')
]