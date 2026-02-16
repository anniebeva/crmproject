from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, AttachUserToCompanySerializer

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from companies.models import Company
from companies.permissions import CompanyPermission

User = get_user_model()

class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class AttachUserToCompanyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated, CompanyPermission]
    serializer_class = AttachUserToCompanySerializer

    def post(self, request):
        owner = request.user
        return Response({'error': 'Only company owner can add employees'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_company_owner:
            return Response({'error': 'This user owns another company'}, status=status.HTTP_400_BAD_REQUEST)

        if user.company is not None:
            return Response({'error': 'This user already belongs to a company'}, status=status.HTTP_400_BAD_REQUEST)

        user.company = owner.company
        user.save()
