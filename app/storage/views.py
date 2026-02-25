from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Storage
from .serializers import StorageSerializer
from .permissions import StoragePermission
from companies.models import Company


class StorageCreateView(generics.CreateAPIView):
    """Create new storage"""

    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]


class StorageDetailView(generics.RetrieveAPIView):
    """Review storage detail"""

    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(
            company=self.request.user.company
        )

class StorageDeleteView(generics.DestroyAPIView):
    """Delete storage"""

    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(
            company=self.request.user.company
        )


class StorageEditView(generics.UpdateAPIView):
    """Edit storage detail"""

    serializer_class =  StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(
            company=self.request.user.company
        )