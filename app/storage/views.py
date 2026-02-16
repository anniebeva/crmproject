from django.shortcuts import render
from rest_framework import generics, permissions, status
from .models import Storage
from .serializers import StorageSerializer
from .permissions import StoragePermission
from companies.models import Company


class StorageCreateView(generics.CreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

class StorageDetailView(generics.RetrieveAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(company=self.request.user.company)


class StorageDeleteView(generics.DestroyAPIView):
    serializer_class = StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(company=self.request.user.company)


class StorageEditView(generics.UpdateAPIView):
    serializer_class =  StorageSerializer
    permission_classes = [permissions.IsAuthenticated, StoragePermission]

    def get_queryset(self):
        return Storage.objects.filter(company=self.request.user.company)