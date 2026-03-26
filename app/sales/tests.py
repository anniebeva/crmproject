import pytest
from django.urls import reverse

from authenticate.models import User
from companies.models import Company
from products.models import Product
from .models import Sale, ProductSale

#Create POST

@pytest.mark.django_db
def test_create_sale_owner_success(api_client, owner_with_supply, test_product_owner):
    """Owner can create sale"""

    api_client.force_authenticate(user=owner_with_supply)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 2}
        ]
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

    test_product_owner.refresh_from_db()
    assert test_product_owner.quantity == 3
    assert Sale.objects.count() == 1

@pytest.mark.django_db
def test_create_sale_employee_success(api_client, employee_with_supply, test_product_employee):
    """Employee can create sale item"""

    api_client.force_authenticate(user=employee_with_supply)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_employee.id, 'quantity': 2}
        ]
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

    test_product_employee.refresh_from_db()
    assert test_product_employee.quantity == 3
    assert Sale.objects.count() == 1

@pytest.mark.django_db
def test_create_sale_diff_employee_error(api_client, owner_with_supply,
                                         foreign_company_employee, test_product_owner):
    """Error: Employee of a different company cannot access sale"""

    api_client.force_authenticate(user=foreign_company_employee)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 2}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_create_sale_unauthorized_error(api_client, owner_with_supply, test_product_owner):
    """Error: Unauthorized user cannot create a sale"""

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 2}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_sale_invalid_date(api_client, owner_with_supply, test_product_owner):
    """Error: Cannot create sale with invalid sale_date"""

    api_client.force_authenticate(user=owner_with_supply)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': 'invalid_date',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 2}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'sale_date' in response.data


@pytest.mark.django_db
def test_create_sale_negative_quantity(api_client, owner_with_supply, test_product_owner):
    """Error: quantity cannot be negative number"""

    api_client.force_authenticate(user=owner_with_supply)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': -2}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'quantity' in str(response.data)


@pytest.mark.django_db
def test_create_sale_excess_quantity_error(api_client, owner_with_supply, test_product_owner):
    """Error: quantity cannot be higher than product in stock"""

    api_client.force_authenticate(user=owner_with_supply)

    url = reverse('sale-create')
    data = {
        'buyer_name': 'Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 20,
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 7}
        ]
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'quantity' in str(response.data)


#View all sales GET

@pytest.mark.django_db
def test_list_sales_owner_success(api_client, owner_with_sales):
    """Owner can see list of sales"""

    api_client.force_authenticate(user=owner_with_sales)

    url = reverse('sales-list')
    response = api_client.get(url)

    print(response.data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_sales_employee_success(api_client, employee_with_sales):
    """Employee can see list of sales"""

    api_client.force_authenticate(user=employee_with_sales)

    url = reverse('sales-list')
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_sales_list_unauthorized_error(api_client, owner_with_sales):
    """Error: Unauthorized user cannot view sales list"""

    url = reverse('sales-list')
    response = api_client.get(url)

    assert response.status_code == 401


#View sale's details GET

@pytest.mark.django_db
def test_view_sale_owner_success(api_client, owner_with_sales, test_product_owner):
    """Owner can view sale's details for their company"""

    api_client.force_authenticate(user=owner_with_sales)

    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-detail', args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == sale.id
    assert response.data['company'] == owner_with_sales.company.id

    products_info = response.data['products_info']
    assert len(products_info) > 0
    assert products_info[0]['quantity'] == 2

    test_product_owner.refresh_from_db()
    assert test_product_owner.quantity == 3

@pytest.mark.django_db
def test_view_sale_employee_success(api_client, employee_with_sales, test_product_employee):
    """Employee can view sale's details for their company"""

    api_client.force_authenticate(user=employee_with_sales)

    sale = employee_with_sales.company.sales.first()

    url = reverse('sale-detail', args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == sale.id
    assert response.data['company'] == employee_with_sales.company.id

    products_info = response.data['products_info']
    assert len(products_info) > 0
    assert products_info[0]['quantity'] == 2

    test_product_employee.refresh_from_db()
    assert test_product_employee.quantity == 3

@pytest.mark.django_db
def test_view_sale_diff_employee_error(api_client, owner_with_sales, foreign_company_employee):
    """Error: Employee of a different company cannot view sale's details"""

    api_client.force_authenticate(user=foreign_company_employee)

    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-detail', args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_view_sale_unauthorized_error(api_client, owner_with_sales):
    """Error: unauthorized users cannot access sale's details"""

    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-detail', args=[sale.id])
    response = api_client.get(url)

    assert response.status_code == 401

#Edit sale PUT

@pytest.mark.django_db
def test_edit_sale_owner_success(api_client, owner_with_sales, test_product_owner):
    """Owner can edit sale's details for their company"""

    api_client.force_authenticate(user=owner_with_sales)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01'
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    sale.refresh_from_db()

    assert sale.buyer_name == 'Other Test Buyer'

@pytest.mark.django_db
def test_edit_sale_employee_success(api_client, employee_with_sales, test_product_employee):
    """Employee can edit sale's details for their company"""

    api_client.force_authenticate(user=employee_with_sales)
    sale = employee_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01'
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    sale.refresh_from_db()

    assert sale.buyer_name == 'Other Test Buyer'


@pytest.mark.django_db
def test_edit_sale_diff_employee_error(api_client, owner_with_sales,
                                       foreign_company_employee, test_product_owner):
    """Error: Employee of a different company cannot edit sale's details"""

    api_client.force_authenticate(user=foreign_company_employee)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01'
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 404

@pytest.mark.django_db
def test_edit_sale_unauthorized_error(api_client, owner_with_sales, test_product_owner):
    """Error: Unauthorized user cannot edit sale's details"""

    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01'
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_sale_edit_invalid_date_error(api_client, owner_with_sales, test_product_owner):
    """Error: Cannot edit sale's details with invalid date"""

    api_client.force_authenticate(user=owner_with_sales)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': 'invalid_date'
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'sale_date' in response.data


@pytest.mark.django_db
def test_sale_edit_product_qty_error(api_client, owner_with_sales, test_product_owner):
    """Error: Cannot edit product quantity through sale's edit"""

    api_client.force_authenticate(user=owner_with_sales)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01',
        'product_sales': [
            {'product': test_product_owner.id, 'quantity': 10}
        ]
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'quantity' in str(response.data)

    test_product_owner.refresh_from_db()
    assert test_product_owner.quantity == 3

@pytest.mark.django_db
def test_sale_edit_discount_error(api_client, owner_with_sales, test_product_owner):
    """Error: Cannot edit discount through sale's edit"""

    api_client.force_authenticate(user=owner_with_sales)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-edit', args=[sale.id])
    data = {
        'buyer_name': 'Other Test Buyer',
        'sale_date': '2026-03-01',
        'discount': 10
    }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'discount' in str(response.data)

    test_product_owner.refresh_from_db()
    assert sale.discount == 20


#Delete sale DELETE

@pytest.mark.django_db
def test_delete_sale_owner_success(api_client, owner_with_sales):
    """Owner can delete sale for their company, qty gets rolled back to previous number"""

    api_client.force_authenticate(user=owner_with_sales)

    sale = owner_with_sales.company.sales.first()

    sale_item = sale.sales_items.first()
    product = sale_item.product

    old_qty = product.quantity
    sale_qty = sale_item.quantity

    url = reverse('sale-delete', args=[sale.id])
    response = api_client.delete(url)

    assert response.status_code == 204

    product.refresh_from_db()
    assert product.quantity == old_qty + sale_qty


@pytest.mark.django_db
def test_delete_sale_employee_success(api_client, employee_with_sales):
    """Employee can delete sale for their company, qty gets rolled back to previous number"""

    api_client.force_authenticate(user=employee_with_sales)

    sale = employee_with_sales.company.sales.first()

    sale_item = sale.sales_items.first()
    product = sale_item.product

    old_qty = product.quantity
    sale_qty = sale_item.quantity

    url = reverse('sale-delete', args=[sale.id])
    response = api_client.delete(url)

    assert response.status_code == 204

    product.refresh_from_db()
    assert product.quantity == old_qty + sale_qty


@pytest.mark.django_db
def test_delete_sale_diff_employee_error(api_client, owner_with_sales, foreign_company_employee):
    """Error: Employee of a different company cannot delete a sale's item"""

    api_client.force_authenticate(user=foreign_company_employee)
    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-delete', args=[sale.id])
    response = api_client.delete(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_delete_sale_unauthorized_error(api_client, owner_with_sales):
    """Error: Unauthorized user cannot delete a supply"""

    sale = owner_with_sales.company.sales.first()

    url = reverse('sale-delete', args=[sale.id])
    response = api_client.delete(url)

    assert response.status_code == 401


#test Analytics

@pytest.mark.django_db
def test_top_products_sales_success(api_client, owner_with_several_sales):
    """Test analytics for top products by sales"""

    api_client.force_authenticate(user=owner_with_several_sales)
    url = reverse('top5-sales')

    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data['count'] == 5


@pytest.mark.django_db
def test_top_product_sales_zero_sales(api_client, employee_with_empty_company):
    """Review statistics with zero sales"""
    api_client.force_authenticate(user=employee_with_empty_company)
    url = reverse('top5-sales')

    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['count'] == 0

@pytest.mark.django_db
def test_top_product_sales_unauthorized_error(api_client, owner_with_several_sales):
    """Error: unauthorized users cannot review analytics"""

    url = reverse('top5-sales')
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_top_products_profit_success(api_client, owner_with_several_sales):
    """Test analytics for top products by profit"""

    api_client.force_authenticate(user=owner_with_several_sales)
    url = reverse('top5-profit')

    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data['count'] == 5


@pytest.mark.django_db
def test_top_product_profit_zero_sales(api_client, employee_with_empty_company):
    """Review statistics with zero sales"""
    api_client.force_authenticate(user=employee_with_empty_company)
    url = reverse('top5-profit')

    response = api_client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert data['count'] == 0


@pytest.mark.django_db
def test_top_product_profit_unauthorized_error(api_client, owner_with_several_sales):
    """Error: unauthorized users cannot review analytics"""

    url = reverse('top5-profit')
    response = api_client.get(url)

    assert response.status_code == 401


@pytest.mark.django_db
def test_profit_analytics_success(api_client, owner_with_several_sales):
    """Test profit analytics with date filtering"""

    api_client.force_authenticate(user=owner_with_several_sales)

    url = reverse('profit-analytics')

    response = api_client.get(url,
                              {'start_date': '2026-07-03',
                               'end_date': '2026-07-04'})

    assert response.status_code == 200

    data = response.json()['results']
    assert float(data[0]['total_profit']) > 0

@pytest.mark.django_db
def test_profit_analytics_zero_sales(api_client, employee_with_empty_company):
    """Test analytics with zero sales"""

    api_client.force_authenticate(user=employee_with_empty_company)

    url = reverse('profit-analytics')

    response = api_client.get(url,
                              {'start_date': '2026-07-03',
                               'end_date': '2026-07-04'})

    assert response.status_code == 200

    data = response.json()['results']
    assert data == []


@pytest.mark.django_db
def test_profit_analytics_unauthorized_error(api_client):
    """Error: unauthorized users cannot review analytics"""

    url = reverse('profit-analytics')
    response = api_client.get(url,
                              {'start_date': '2026-07-03',
                               'end_date': '2026-07-04'})

    assert response.status_code == 401





