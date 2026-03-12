from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.db import transaction
from decimal import Decimal

from .models import Sale, SaleProduct
from products.models import Product
from utils import calculate_price_at_sale

class SaleProductSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    def validate_product(self, product):
        user = self.context['request'].user

        if product.storage.company != user.company:
            raise serializers.ValidationError(
                'This product belongs to another company'
            )

        return product


class SaleSerializer(serializers.ModelSerializer):
    products = SaleProductSerializer(many=True, write_only=True)
    products_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Sale
        read_only_fields = ['id', 'company']
        fields = ['id', 'company','buyer_name', 'sale_date', 'discount', 'products', 'products_info']

    def __init__(self, *args, **kwargs):
        """Make products not required to enter in case of edit"""

        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['products'].required = False

    def validate_company(self, company):
        user = self.context['request'].user

        if company != user.company:
            raise serializers.ValidationError(
                'You cannot create sale for another company'
            )

        return company

    def get_products_info(self, obj):
        """Get information about products in the supply"""

        return [
            {
                'product': sp.product.id,
                'title': sp.product.title,
                'quantity': sp.quantity,
                'price_at_sale': sp.price_at_sale
            }
            for sp in obj.sales_items.all()
        ]

    def create(self, validated_data):
        product_data = validated_data.pop('products')
        user = self.context['request'].user

        errors = {}

        for p in product_data:
            product = p['product']

            if product.quantity < p['quantity']:
                errors[f'quantity: Not enough {product.title}'] = product.quantity

        if errors:
            raise serializers.ValidationError(errors)

        with transaction.atomic():
            sale = Sale.objects.create(
                company=user.company,
                **validated_data
            )

            for p in product_data:

                price_at_sale = calculate_price_at_sale(p['product'].sale_price, sale.discount)

                SaleProduct.objects.create(
                    sale=sale,
                    product=p['product'],
                    quantity=p['quantity'],
                    price_at_sale=price_at_sale
                )

            sale.apply()

        return sale


    def update(self, instance, validated_data):
        """Update product quantity and SupplyProduct model"""

        instance.buyer_name = validated_data.get('buyer_name', instance.buyer_name)
        instance.sale_date = validated_data.get('sale_date', instance.sale_date)
        discount = validated_data.get('discount')

        if discount is not None:
            instance.discount = Decimal(discount)
            instance.save()
            instance.recalc_price_at_sale()

        if 'products' in validated_data:
            raise serializers.ValidationError(
                'Cannot change product\'s details (quantity, price, etc.) in existing sale. Delete sale and create a new one.'
            )

        instance.save()
        return instance


class TopProductSalesSerializer(serializers.Serializer):
    product__id = serializers.IntegerField()
    product__title = serializers.CharField()
    total_sales = serializers.IntegerField()

class TopProductProfitSerializer(serializers.Serializer):
    product__id = serializers.IntegerField()
    product__title = serializers.CharField()
    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)

class ProfitAnalyticsSerializer(serializers.Serializer):
    sale__sale_date = serializers.DateField()
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2)