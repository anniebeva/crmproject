from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from .models import Storage

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        read_only_fields = ['id']
        fields = ['id', 'address', 'company_id']

    def create(self, validated_data):
        user = self.context['request'].user

        if not user.is_company_owner:
            raise ValidationError('This user cannot access storage')

        company = user.company

        if hasattr(company, 'storage'):
            raise ValidationError('Company already has a storage')

        return Storage.objects.create(company=company, **validated_data)

