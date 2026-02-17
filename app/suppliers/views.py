from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Supplier
from .serializers import SupplierSerializer
from companies.models import Company

class SupplierCreateView(generics.CreateAPIView):
    """Create new supplier"""

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplierDetailView(generics.RetrieveAPIView):
    """Review supplier's detail"""

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)


class SupplierDeleteView(generics.DestroyAPIView):
    """Delete supplier"""

    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)


class SupplierEditView(generics.UpdateAPIView):
    """Edit supplier's detail"""
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Supplier.objects.filter(company=self.request.user.company)