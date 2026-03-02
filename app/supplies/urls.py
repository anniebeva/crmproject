from django.urls import path
from .views import SupplyCreateView, SupplyEditView, SupplyDeleteView, SupplyDetailView, SupplyListView

urlpatterns = [
    path('create/', SupplyCreateView.as_view(), name='supply-create'),
    path('list/', SupplyListView.as_view(), name='supply-list'),
    path('<int:pk>/', SupplyDetailView.as_view(), name='supply-detail'),
    path('<int:pk>/edit/', SupplyEditView.as_view(), name='supply-edit'),
    path('<int:pk>/delete/', SupplyDeleteView.as_view(), name='supply-delete'),
]
