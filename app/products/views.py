from rest_framework import generics, permissions, status

from .models import Product
from .serializers import ProductSerializer
from .permissions import ProductPermission
from storage.models import Storage

class ProductCreateView(generics.CreateAPIView):
    """Create new product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

class ProductListView(generics.ListAPIView):
    """View all products"""

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

    def get_queryset(self):
        return Product.objects.filter(
            storage__company=self.request.user.company
        )

class ProductDetailView(generics.RetrieveAPIView):
    """View Product details"""

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]
    def get_queryset(self):
        return Product.objects.filter(
            storage__company=self.request.user.company
        )

class ProductEditView(generics.UpdateAPIView):
    """Edit products detail"""

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

    def get_queryset(self):
        return Product.objects.filter(
            storage__company=self.request.user.company
        )

class ProductDeleteView(generics.DestroyAPIView):
    """Delete product detail"""

    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

    def get_queryset(self):
        return Product.objects.filter(
            storage__company=self.request.user.company
        )
