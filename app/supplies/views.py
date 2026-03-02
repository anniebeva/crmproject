from django.shortcuts import render
from .models import Supply
from .serializers import SupplySerializer
from .permissions import SupplyPermissions
from suppliers.models import Supplier
from rest_framework import generics, permissions

class SupplyCreateView(generics.CreateAPIView):
    """Create new supply record"""

    queryset = Supply.objects.all()
    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, SupplyPermissions]

class SupplyListView(generics.ListAPIView):
    """Review list of supplies"""

    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, SupplyPermissions]

    def get_queryset(self):
        return Supply.objects.filter(
            supplier__company=self.request.user.company
        )

class SupplyDetailView(generics.RetrieveAPIView):
    """Review supply's detail"""

    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, SupplyPermissions]

    def get_queryset(self):
        return Supply.objects.filter(
            supplier__company=self.request.user.company
        )


class SupplyEditView(generics.UpdateAPIView):
    """Edit supply's detail"""

    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, SupplyPermissions]

    def get_queryset(self):
        return Supply.objects.filter(
            supplier__company=self.request.user.company
        )


class SupplyDeleteView(generics.DestroyAPIView):
    """Delete supply's detail"""

    serializer_class = SupplySerializer
    permission_classes = [permissions.IsAuthenticated, SupplyPermissions]

    def get_queryset(self):
        return Supply.objects.filter(
            supplier__company=self.request.user.company
        )

