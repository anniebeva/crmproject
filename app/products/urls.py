from django.urls import path
from.views import ProductCreateView, ProductDetailView, ProductEditView, ProductDeleteView, ProductListView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('list/', ProductListView.as_view(), name='products-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/edit/', ProductEditView.as_view(), name='product-edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete')
]