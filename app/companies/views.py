from rest_framework import generics, permissions, status
from rest_framework.response import Response
from authenticate.models import User
from .models import Company
from .permissions import CompanyPermission
from .serializers import CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

class CompanyDetailView(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(company=self.request.user.company)


class CompanyDeleteView(generics.DestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(company=self.request.user.company)


class CompanyEditView(generics.UpdateAPIView):
    serializer_class =  CompanySerializer
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]

    def get_queryset(self):
        return Company.objects.filter(company=self.request.user.company)

