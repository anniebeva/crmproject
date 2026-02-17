from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        read_only_fields = ['id']
        fields = ['id', 'title', 'INN']


    def create(self, validated_data):
        user = self.context['request'].user
        company = user.company

        return Supplier.objects.create(company=company, **validated_data)
