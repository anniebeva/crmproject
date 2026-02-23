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

class ProductDetailView(generics.RetrieveAPIView):
    """View Product details"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

class ProductEditView(generics.UpdateAPIView):
    """Edit products detail"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]

class ProductDeleteView(generics.DestroyAPIView):
    """Delete product detail"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, ProductPermission]
