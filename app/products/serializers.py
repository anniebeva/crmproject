from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        read_only_fields = ['id', 'quantity']
        fields = ['id', 'title', 'purchase_price', 'sale_price', 'storage', 'quantity']

    def validate_storage(self, value):
        user = self.context['request'].user
        if value.company != user.company:
            raise serializers.ValidationError('Storage should belong to the company')
        return value

    def validate_purchase_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price cannot be negative')
        return price

    def validate_sale_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price cannot be negative')
        return price

