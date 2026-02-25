import pytest
from django.urls import reverse

from authenticate.models import User
from storage.models import Storage
from .models import Product


# Create product POST

@pytest.mark.django_db
def test_create_product_owner_success(api_client, owner_with_storage):
    """Owner can create a product for their company storage"""

    api_client.force_authenticate(user=owner_with_storage)
    storage = owner_with_storage.company.storage

    url = reverse('product-create')
    data = {
        'title': 'Test Product',
        'purchase_price': 50.0,
        'sale_price': 80.0,
        'storage': storage.id
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == 'Test Product'
    assert response.data['quantity'] == 0


@pytest.mark.django_db
def test_create_product_employee_success(api_client, employee_with_storage):
    """Employee can create a product for their company storage"""

    api_client.force_authenticate(employee_with_storage)
    storage = employee_with_storage.company.storage

    url = reverse('product-create')
    data = {
        'title': 'Test Product',
        'purchase_price': 50.0,
        'sale_price': 80.0,
        'storage': storage.id
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['title'] == 'Test Product'

@pytest.mark.django_db
def test_create_product_diff_employee_error(api_client, owner_with_storage, foreign_company_employee):
    """Error: employee of another company cannot create product"""

    api_client.force_authenticate(foreign_company_employee)
    storage = owner_with_storage.company.storage

    data = {
        'title': 'Test Product',
        'purchase_price': 50.0,
        'sale_price': 80.0,
        'storage': storage.id
    }

    url = reverse('storage-create')
    response = api_client.post(url, data, format='json')

    assert response.status_code == 403

@pytest.mark.django_db
def test_create_product_unauthorized_error(api_client, owner_with_storage):
    """Error: unathorized user cannot create product"""

    storage = owner_with_storage.company.storage

    data = {
        'title': 'Test Product',
        'purchase_price': 50.0,
        'sale_price': 80.0,
        'storage': storage.id
    }

    url = reverse('storage-create')
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_create_product_w_negative_purchasing_price_error(api_client, owner_with_storage):
    """Error: Purchase price cannot be negative"""

    api_client.force_authenticate(user=owner_with_storage)
    storage = owner_with_storage.company.storage

    url = reverse('product-create')
    data = {
        'title': 'Test Product',
        'purchase_price': -50.0,
        'sale_price': 80.0,
        'storage': storage.id
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 400

@pytest.mark.django_db
def test_create_product_w_negative_sale_price_error(api_client, owner_with_storage):
    """Error: Sale price cannot be negative"""

    api_client.force_authenticate(user=owner_with_storage)
    storage = owner_with_storage.company.storage

    url = reverse('product-create')
    data = {
        'title': 'Test Product',
        'purchase_price': 50.0,
        'sale_price': -80.0,
        'storage': storage.id
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == 400


#View list of products GET
@pytest.mark.django_db
def test_list_products_owner_success(api_client, owner_with_product):
    """Owner can see list of products"""

    api_client.force_authenticate(user=owner_with_product)

    url = reverse('products-list')
    response = api_client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_list_products_employee_success(api_client, employee_with_product):
    """Employee can see list of products"""

    api_client.force_authenticate(user=employee_with_product)

    url = reverse('products-list')
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_product_unauthorized_error(api_client, owner_with_product):
    """Error: Unauthorized user cannot view products list"""

    url = reverse('products-list')
    response = api_client.get(url)

    assert response.status_code == 401

# View product GET

@pytest.mark.django_db
def test_view_product_owner_success(api_client, owner_with_product):
    """Owner can view their company's product"""
    api_client.force_authenticate(user=owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == product.id
    assert response.data['storage'] == product.storage.id

@pytest.mark.django_db
def test_view_product_employee_success(api_client, employee_with_product):
    """Employee can view their company's product"""
    api_client.force_authenticate(user=employee_with_product)
    storage = employee_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == product.id
    assert response.data['storage'] == product.storage.id

@pytest.mark.django_db
def test_view_product_diff_employee_error(api_client, owner_with_product, foreign_company_employee):
    """Employee of another company cannot view product"""
    api_client.force_authenticate(user=foreign_company_employee)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_view_product_unauthorized_error(api_client, owner_with_product):
    """Error: Unauthorized user cannot view product"""
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-detail', args=[product.id])
    response = api_client.get(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_view_product_nonexist_error(api_client, owner_with_product):
    """Error: Nonexistent product returns 404"""

    api_client.force_authenticate(user=owner_with_product)
    invalid_id = 9999

    url = reverse('product-detail', args=[invalid_id])
    response = api_client.get(url)
    assert response.status_code == 404


# Edit product PUT
@pytest.mark.django_db
def test_edit_product_owner_success(api_client, owner_with_product):
    """Owner can edit their company's product"""

    api_client.force_authenticate(user=owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-edit', args=[product.id])
    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 200

    product.refresh_from_db()
    assert product.title == 'Updated Product'


@pytest.mark.django_db
def test_edit_product_employee_success(api_client, employee_with_product):
    """Employee can edit their company's product"""

    api_client.force_authenticate(user=employee_with_product)
    storage = employee_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-edit', args=[product.id])
    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 200

    product.refresh_from_db()
    assert product.title == 'Updated Product'


@pytest.mark.django_db
def test_edit_product_foreign_storage_error(api_client, owner_with_product, foreign_company_employee):
    """Error: product cannot be moved to foreign storage"""

    api_client.force_authenticate(user=owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    foreign_storage = Storage.objects.create(
        address='storage address',
        company=foreign_company_employee.company
    )


    url = reverse('product-edit', args=[product.id])
    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': foreign_storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 400

@pytest.mark.django_db
def test_edit_product_diff_employee_error(api_client, owner_with_product, foreign_company_employee):
    """Employee of another company cannot edit product"""

    api_client.force_authenticate(user=foreign_company_employee)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    url = reverse('product-edit', args=[product.id])
    response = api_client.put(url, data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_product_unauthorized_error(api_client, owner_with_product):
    """Error: Unauthorized user cannot edit product"""

    storage = owner_with_product.company.storage
    product = storage.products.first()

    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    url = reverse('product-edit', args=[product.id])
    response = api_client.put(url, data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_edit_product_negative_purchase_price_error(api_client, owner_with_product):
    """Error: Purchase price cannot be negative"""

    api_client.force_authenticate(owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-edit', args=[product.id])
    data = {
        'title': 'Updated Product',
        'purchase_price': -51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 400

def test_edit_product_negative_sale_price_error(api_client, owner_with_product):
    """Error: Sale price cannnot be negative"""

    api_client.force_authenticate(owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-edit', args=[product.id])
    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': -81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 400

def test_edit_product_nonexist_error(api_client, owner_with_product):
    """Error: Nonexistent product returns 404"""

    api_client.force_authenticate(owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    invalid_id = 9999
    url = reverse('product-edit', args=[invalid_id])
    data = {
        'title': 'Updated Product',
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    assert response.status_code == 404

def test_edit_product_quantity_unchanged(api_client, owner_with_product):
    """Quantity cannot be edited directly"""

    api_client.force_authenticate(owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    invalid_id = 9999
    url = reverse('product-edit', args=[invalid_id])
    data = {
        'title': 'Updated Product',
        'quntity': 5,
        'purchase_price': 51.0,
        'sale_price': 81.0,
        'storage': storage.id
    }

    response = api_client.put(url, data)
    product.refresh_from_db()
    assert product.quantity == 0



# Delete product DELETE

@pytest.mark.django_db
def test_delete_product_owner_success(api_client, owner_with_product):
    """Owner can delete their company's product"""

    api_client.force_authenticate(user=owner_with_product)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-delete', args=[product.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Product.objects.filter(id=product.id).exists()

@pytest.mark.django_db
def test_delete_product_employee_success(api_client, employee_with_product):
    """Employee can delete their company's product"""
    api_client.force_authenticate(user=employee_with_product)
    storage = employee_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-delete', args=[product.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Product.objects.filter(id=product.id). exists()

@pytest.mark.django_db
def test_delete_product_diff_employee_error(api_client, owner_with_product, foreign_company_employee):
    """Employee of another company cannot delete product"""

    api_client.force_authenticate(user=foreign_company_employee)
    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-delete', args=[product.id])
    response = api_client.delete(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_product_unauthorized_error(api_client, owner_with_product):
    """Error: Unauthorized user cannot delete product"""

    storage = owner_with_product.company.storage
    product = storage.products.first()

    url = reverse('product-delete', args=[product.id])
    response = api_client.delete(url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_delete_product_nonexist_error(api_client, owner_with_product):
    """Error: Nonexistent product returns 404"""

    api_client.force_authenticate(user=owner_with_product)
    invalid_id = 9999

    url = reverse('product-delete', args=[invalid_id])
    response = api_client.delete(url)
    assert response.status_code == 404