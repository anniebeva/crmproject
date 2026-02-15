from django.shortcuts import render

# Create your views here.

from rest_framework import generics, permissions
from .models import Company
from .serializers import CompanySerializer

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]