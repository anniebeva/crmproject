from django.urls import path
from drf_spectacular.utils import extend_schema_view, extend_schema
from .views import (SaleCreateView, SaleEditView, SaleDeleteView, SaleDetailView, SalesListView,
                    TopProductsSalesView, TopProductsProfitView, ProfitAnalyticsView)


urlpatterns = [
    path('create/', SaleCreateView.as_view(), name='sale-create'),
    path('list/', SalesListView.as_view(), name='sales-list'),
    path('<int:pk>/', SaleDetailView.as_view(), name='sale-detail'),
    path('<int:pk>/edit/', SaleEditView.as_view(), name='sale-edit'),
    path('<int:pk>/delete/', SaleDeleteView.as_view(), name='sale-delete'),

    path('analytics/profit/',
        extend_schema_view(get=extend_schema(tags=['analytics']))
        (ProfitAnalyticsView.as_view()),
        name='profit-analytics'),
    path('analytics/top-products/',
        extend_schema_view(get=extend_schema(tags=['analytics']))
        (TopProductsSalesView.as_view()),
        name='top5-sales'),
    path('analytics/top-profit/',
        extend_schema_view(get=extend_schema(tags=['analytics']))
        (TopProductsProfitView.as_view()),
        name='top5-profit')
]
