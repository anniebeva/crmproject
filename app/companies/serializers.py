from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        read_only_fields = ['id']
        fields = ['id', 'INN', 'title']


    def create(self, validated_data):
        user = self.context['request'].user

        if user.is_company_owner:
            raise serializers.ValidationError('User already owns a company')

        company = Company.objects.create(**validated_data)
        user.company = company
        user.is_company_owner = True
        user.save()

        return company



