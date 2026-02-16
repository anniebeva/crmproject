from django.urls import path
from .views import StorageCreateView, StorageDeleteView, StorageDetailView, StorageEditView


urlpatterns = [
    path('create/', StorageCreateView.as_view(), name='storage-create'),
    path('<int:pk>/', StorageDetailView.as_view(), name='storage-detail'),
    path('<int:ps>/edit/', StorageEditView.as_view(), name='storage-edit'),
    path('<int:pk>/delete/', StorageDeleteView.as_view(), name='storage-delete')
]
