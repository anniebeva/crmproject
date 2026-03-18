from django.db.models import Sum, F
from rest_framework import generics, permissions
from datetime import date, timedelta, datetime

from .permissions import SalePermissions
from .serializers import SaleSerializer, TopProductSalesSerializer, TopProductProfitSerializer, ProfitAnalyticsSerializer
from .models import Sale, ProductSale


class SaleCreateView(generics.CreateAPIView):
    """Create new sale"""
    serializer_class = SaleSerializer
    queryset = Sale.objects.all()
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

class SalesListView(generics.ListAPIView):
    """View list of sales"""

    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        queryset = Sale.objects.filter(
            company=self.request.user.company
        )

        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(sale_date__gte=start_date)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(sale_date__gte=end_date)

        return queryset


class SaleDetailView(generics.RetrieveAPIView):
    """View sale's detail"""

    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        return Sale.objects.filter(
            company=self.request.user.company
        )

class SaleEditView(generics.UpdateAPIView):
    """Edit sale's detail"""

    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        return Sale.objects.filter(
            company=self.request.user.company
        )

class SaleDeleteView(generics.DestroyAPIView):
    """Delete sale"""

    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        return Sale.objects.filter(
            company=self.request.user.company
        )


class TopProductsSalesView(generics.ListAPIView):
    """View list of top 5 products by n of Sales"""

    serializer_class =  TopProductSalesSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        return (
            ProductSale.objects
            .filter(sale__company=self.request.user.company)
            .values('product__id', 'product__title')
            .annotate(total_sales=Sum('quantity'))
            .order_by('-total_sales')[:5]
        )


class TopProductsProfitView(generics.ListAPIView):
    """View list of top 5 products by profit"""

    serializer_class = TopProductProfitSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        return (
            ProductSale.objects
            .filter(sale__company=self.request.user.company)
            .values('product__id', 'product__title')
            .annotate(total_profit=Sum(
                (F('price_at_sale') - F('product__purchase_price')) * F('quantity')
            ))
            .order_by('-total_profit')[:5]
        )


class ProfitAnalyticsView(generics.ListAPIView):
    """View analytics of profit for a specific time period"""
    serializer_class = ProfitAnalyticsSerializer
    permission_classes = [permissions.IsAuthenticated, SalePermissions]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        queryset = ProductSale.objects.filter(sale__company=self.request.user.company)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = date.today() - timedelta(days=30)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = date.today()

        queryset = queryset.filter(sale__sale_date__range=[start_date, end_date])

        return (
            queryset
            .values('sale__sale_date')
            .annotate(total_profit=Sum(
                (F('price_at_sale') - F('product__purchase_price')) * F('quantity')
            ))
            .order_by('sale__sale_date')
        )