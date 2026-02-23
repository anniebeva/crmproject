from rest_framework import serializers
from .models import Supply


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        read_only_fields = ['id']
        fields = ['id', 'supplier', 'delivery_date']

    def validate_supplier(self, supplier):
        user = self.context['request'].user

        if supplier.company != user.company:
            raise serializers.ValidationError(
                'You cannot create supply for another supplier'
            )

        return supplier




