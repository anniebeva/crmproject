from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import Supply, SupplyProduct
from products.models import Product

class SupplyProductSerializer(serializers.Serializer):

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, product):
        user = self.context['request'].user

        if product.storage.company != user.company:
            raise serializers.ValidationError(
                'This product belongs to another company'
            )

        return product


class SupplySerializer(serializers.ModelSerializer):
    products = SupplyProductSerializer(many=True, write_only=True)
    products_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Supply
        read_only_fields = ['id']
        fields = ['id', 'supplier', 'delivery_date', 'products', 'products_info']

    def validate_supplier(self, supplier):
        user = self.context['request'].user

        if supplier.company != user.company:
            raise serializers.ValidationError(
                'You cannot create supply for another supplier'
            )

        return supplier

    def get_products_info(self, obj):
        """Get information about products in the supply"""
        return [
            {
            'product': sp.product.id,
            'title': sp.product.title,
            'quantity': sp.quantity
            }
            for sp in obj.supply_items.all()
        ]

    def create(self, validated_data):
        """Create Supply and SupplyProduct items, update product qty"""

        product_data = validated_data.pop('products')

        supply = Supply.objects.create(**validated_data)

        for p in product_data:
            SupplyProduct.objects.create(
                supply=supply,
                product=p['product'],
                quantity=p['quantity']
            )

        supply.apply()

        return supply


    def update(self, instance, validated_data):
        """Update product quantity and SupplyProduct model"""

        product_data = validated_data.pop('products')
        instance.rollback()

        instance.supplier = validated_data.get('supplier', instance.supplier)
        instance.delivery_date = validated_data.get('delivery_date', instance.delivery_date)
        instance.save()

        instance.supply_items.all().delete()

        for p in product_data:

            SupplyProduct.objects.create(
                supply=instance,
                product=p['product'],
                quantity=p['quantity']
            )

        instance.apply()

        return instance



