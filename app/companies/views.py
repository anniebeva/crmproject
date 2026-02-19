from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authenticate.models import User
from .models import Company
from .permissions import CompanyPermission
from .serializers import CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    """Create new company"""

    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

class CompanyDetailView(generics.RetrieveAPIView):
    """Review company detail. Available to all authenticated users"""

    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    queryset = Company.objects.all()


class CompanyDeleteView(generics.DestroyAPIView):
    """Delete company"""

    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(id=self.request.user.company_id)


class CompanyEditView(generics.UpdateAPIView):
    """Edit company details"""

    serializer_class =  CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(id=self.request.user.company_id)

