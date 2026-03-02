import pytest
from django.urls import reverse
from datetime import datetime

from authenticate.models import User
from companies.models import Company
from suppliers.models import Supplier
from .models import Supply, SupplyProduct

# Create POST
@pytest.mark.django_db
def test_create_supply_owner_success(api_client, owner_with_supplier, test_product_owner):
    """Owner can create a supply for their company"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()
    test_product = test_product_owner

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product.id, 'quantity': 5}
                ]
            }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

    test_product.refresh_from_db()
    assert test_product.quantity == 5
    assert Supply.objects.count() == 1

@pytest.mark.django_db
def test_create_supply_employee_success(api_client, employee_with_supplier, test_product_employee):
    """Employee can create a supply for their company"""

    api_client.force_authenticate(user=employee_with_supplier)
    supplier = employee_with_supplier.company.suppliers.first()
    test_product = test_product_employee

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product.id, 'quantity': 5}
                ]
            }
    response = api_client.post(url, data, format='json')
    print(employee_with_supplier.company)
    print(test_product.storage.company)

    assert response.status_code == 201
    test_product.refresh_from_db()
    assert test_product.quantity == 5
    assert Supply.objects.count() == 1


@pytest.mark.django_db
def test_create_supply_diff_employee_error(api_client, owner_with_supplier,
                                           foreign_company_employee, test_product_owner):
    """Error: Employee of a different company cannot create a supply"""

    api_client.force_authenticate(user=foreign_company_employee)
    supplier = owner_with_supplier.company.suppliers.first()
    test_product = test_product_owner

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product.id, 'quantity': 5}
                ]
            }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_supply_unathorized_error(api_client, owner_with_supplier, test_product_owner):
    """Error: Unauthorized user cannot create a supply"""

    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 5}
                ]
            }
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_create_supply_invalid_date_error(api_client, owner_with_supplier, test_product_owner):
    """Cannot create supply with invalid delivery_date"""

    api_client.force_authenticate(user=owner_with_supplier)

    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': 'invalid_date',
            'products': [
                    {'product_id': test_product_owner.id, 'quantity': 5}
                ]
            }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'delivery_date' in response.data

@pytest.mark.django_db
def test_create_supply_negative_quantity(api_client, owner_with_supplier, test_product_owner):
    """Error: qunatity cannot be negative number"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': -5}
                ]
            }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'quantity' in str(response.data)


#View list of supplies GET
@pytest.mark.django_db
def test_list_supplies_owner_success(api_client, owner_with_supply):
    """Owner can see list of supplies"""

    api_client.force_authenticate(user=owner_with_supply)

    url = reverse('supply-list')
    response = api_client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_list_supplies_employee_success(api_client, employee_with_supply):
    """Employee can see list of supplies"""

    api_client.force_authenticate(user=employee_with_supply)

    url = reverse('supply-list')
    response = api_client.get(url)

    assert response.status_code == 200


@pytest.mark.django_db
def test_list_supplies_unauthorized_error(api_client, owner_with_supply):
    """Error: Unauthorized user cannot view supplies list"""

    url = reverse('supply-list')
    response = api_client.get(url)

    assert response.status_code == 401

# View details GET

@pytest.mark.django_db
def test_view_supply_owner_success(api_client, owner_with_supply, test_product_owner):
    """Owner can view a supply for their company"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supply.id
    assert response.data['supplier'] == supplier.id

    products_info = response.data['products_info']
    assert len(products_info) > 0
    assert products_info[0]['quantity'] == 5

    test_product_owner.refresh_from_db()
    assert test_product_owner.quantity == 5

@pytest.mark.django_db
def test_view_supply_employee_success(api_client, employee_with_supply, test_product_employee):
    """Owner can view a supply for their company"""

    api_client.force_authenticate(user=employee_with_supply)

    supplier = employee_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supply.id
    assert response.data['supplier'] == supplier.id

    products_info = response.data['products_info']
    assert len(products_info) > 0
    assert products_info[0]['quantity'] == 5

    test_product_employee.refresh_from_db()
    assert test_product_employee.quantity == 5

@pytest.mark.django_db
def test_view_supply_diff_employee_error(api_client, owner_with_supply, foreign_company_employee):
    """Error: Employee of a different company cannot view a supply"""

    api_client.force_authenticate(user=foreign_company_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 404

@pytest.mark.django_db
def test_view_supply_unathorized_error(api_client, owner_with_supply):
    """Error: unathorized users cannot access suppliers"""

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 401

# Edit details PUT

@pytest.mark.django_db
def test_edit_supply_owner_success(api_client, owner_with_supplier, test_product_owner):
    """Owner can edit a supply for their company"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()

    supply = Supply.objects.create(supplier=supplier, delivery_date='2026-02-01')
    SupplyProduct.objects.create(supply=supply, product=test_product_owner, quantity=5)
    supply.apply()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 10}
                ]
            }
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    test_product_owner.refresh_from_db()
    supply.refresh_from_db()
    assert response.data['delivery_date'] == '2026-02-01'
    assert test_product_owner.quantity == 10

@pytest.mark.django_db
def test_edit_supply_empoyee_success(api_client, employee_with_supplier, test_product_employee):
    """Employee can edit a supply for their company"""

    api_client.force_authenticate(user=employee_with_supplier)

    supplier = employee_with_supplier.company.suppliers.first()

    supply = Supply.objects.create(supplier=supplier, delivery_date='2026-02-01')
    SupplyProduct.objects.create(supply=supply, product=test_product_employee, quantity=5)
    supply.apply()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01',
            'products': [
                    {'product': test_product_employee.id, 'quantity': 10}
                ]
            }
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    test_product_employee.refresh_from_db()
    supply.refresh_from_db()
    assert response.data['delivery_date'] == '2026-02-01'
    assert test_product_employee.quantity == 10


@pytest.mark.django_db
def test_edit_supply_diff_employee_error(api_client, owner_with_supply,
                                         foreign_company_employee, test_product_owner):
    """Error: Employee of a different company cannot edit a supply"""

    api_client.force_authenticate(user=foreign_company_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 10}
                ]
            }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_supplier_unathorized_error(api_client, owner_with_supply, test_product_owner):
    """Error: Unauthorized user cannot edit a supply"""

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 10}
                ]
            }
    response = api_client.put(url, data, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_supply_edit_invalid_date_error(api_client, owner_with_supply, test_product_owner):
    """Error: Cannot edit supply with invalid delivery_date"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': 'invalid_date',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 10}
                ]
            }
    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'delivery_date' in response.data

@pytest.mark.django_db
def test_edit_supply_negative_quantity(api_client, owner_with_supply, test_product_owner):
    """Error: qunatity cannot be negative number"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])

    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': -5}
                ]
            }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'quantity' in str(response.data)

@pytest.mark.django_db
def test_edit_supply_diff_supplier_error(api_client, owner_with_supply,
                                         foreign_company_employee, test_product_owner):
    """Error: Cannot change supply supplier to supplier from another company"""

    api_client.force_authenticate(user=owner_with_supply)

    current_supplier = owner_with_supply.company.suppliers.first()
    supply = current_supplier.supplies.first()


    foreign_supplier = foreign_company_employee.company.suppliers.create(
        title='ForeignSupplier',
        INN='111111111111'
    )

    url = reverse('supply-edit', args=[supply.id])

    data = {'supplier': foreign_supplier.id,
            'delivery_date': '2026-02-01',
            'products': [
                    {'product': test_product_owner.id, 'quantity': 10}
                ]
            }

    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'supplier' in response.data

# Delete supply DELETE
@pytest.mark.django_db
def test_delete_supply_owner_success(api_client, owner_with_supply):
    """Owner can delete a supply for their company"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    supply_item = supply.supply_items.first()
    product = supply_item.product

    old_quantity = product.quantity
    supply_quantity = supply_item.quantity

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 204

    product.refresh_from_db()
    assert product.quantity == old_quantity - supply_quantity

@pytest.mark.django_db
def test_delete_supply_employee_success(api_client, employee_with_supply):
    """Employee can delete a supply for their company"""

    api_client.force_authenticate(user=employee_with_supply)

    supplier = employee_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    supply_item = supply.supply_items.first()
    product = supply_item.product

    old_quantity = product.quantity
    supply_quantity = supply_item.quantity

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 204

    product.refresh_from_db()
    assert product.quantity == old_quantity - supply_quantity

@pytest.mark.django_db
def test_delete_supply_diff_employee_error(api_client, owner_with_supply, foreign_company_employee):
    """Error: Employee of a different company cannot delete a supply"""

    api_client.force_authenticate(foreign_company_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_supply_unathorized_error(api_client, owner_with_supply):
    """Error: Unauthorized user cannot delete a supply"""

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 401




