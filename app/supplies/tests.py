import pytest
from django.urls import reverse
from datetime import datetime

from authenticate.models import User
from companies.models import Company
from suppliers.models import Supplier
from .models import Supply
from utils import create_owner, create_employee

#supplier, delivery_date

# Create POST
@pytest.mark.django_db
def test_create_supply_owner_success(api_client, owner_with_supplier):
    """Owner can create a supply for their company"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

@pytest.mark.django_db
def test_create_supply_employee_success(api_client, employee_with_supplier):
    """Employee can create a supply for their company"""

    api_client.force_authenticate(user=employee_with_supplier)
    supplier = employee_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

@pytest.mark.django_db
def test_create_supply_diff_employee_error(api_client, owner_with_supplier):
    """Error: Employee of a different company cannot create a supply"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108')

    api_client.force_authenticate(user=new_employee)
    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01'}

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_supplier_unathorized_error(api_client, owner_with_supplier):
    """Error: Unauthorized user cannot create a supply"""

    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {'supplier': supplier.id,
            'delivery_date': '2026-03-01'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401

@pytest.mark.django_db
def test_supply_create_invalid_date_error(api_client, owner_with_supplier):
    """Cannot create supply with invalid delivery_date"""

    api_client.force_authenticate(user=owner_with_supplier)

    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supply-create')
    data = {
        'supplier': supplier.id,
        'delivery_date': 'invalid-date'
    }

    response = api_client.post(url, data, format='json')

    assert response.status_code == 400
    assert 'delivery_date' in response.data

# View details GET

@pytest.mark.django_db
def test_view_supply_owner_success(api_client, owner_with_supply):
    """Owner can view a supply for their company"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supply.id
    assert response.data['supplier'] == supplier.id

@pytest.mark.django_db
def test_view_supply_employee_success(api_client, employee_with_supply):
    """Owner can view a supply for their company"""

    api_client.force_authenticate(user=employee_with_supply)

    supplier = employee_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supply.id
    assert response.data['supplier'] == supplier.id

@pytest.mark.django_db
def test_view_supply_diff_employee_error(api_client, owner_with_supply):
    """Error: Employee of a different company cannot view a supply"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108')

    api_client.force_authenticate(user=new_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-detail', args=[supply.id])
    response = api_client.get(url)

    assert response.status_code == 403

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
def test_edit_supply_owner_success(api_client, owner_with_supply):
    """Owner can edit a supply for their company"""

    api_client.force_authenticate(user=owner_with_supply)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    supply.refresh_from_db()
    assert response.data['delivery_date'] == '2026-02-01'

@pytest.mark.django_db
def test_edit_supply_empoyee_success(api_client, employee_with_supply):
    """Employee can edit a supply for their company"""

    api_client.force_authenticate(user=employee_with_supply)
    supplier = employee_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    supply.refresh_from_db()
    assert response.data['delivery_date'] == '2026-02-01'


@pytest.mark.django_db
def test_edit_supply_diff_employee_error(api_client, owner_with_supply):
    """Error: Employee of a different company cannot edit a supply"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108')

    api_client.force_authenticate(user=new_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01'}

    response = api_client.put(url, data, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_supplier_unathorized_error(api_client, owner_with_supply):
    """Error: Unauthorized user cannot edit a supply"""

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': '2026-02-01'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_supply_edit_invalid_date_error(api_client, owner_with_supply):
    """Error: Cannot edit supply with invalid delivery_date"""

    api_client.force_authenticate(user=owner_with_supply)

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-edit', args=[supply.id])
    data = {'supplier': supplier.id,
            'delivery_date': 'invalid_date'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 400
    assert 'delivery_date' in response.data

@pytest.mark.django_db
def test_edit_supply_diff_supplier_error(api_client, owner_with_supply):
    """Error: Cannot change supply supplier to supplier from another company"""

    api_client.force_authenticate(user=owner_with_supply)

    current_supplier = owner_with_supply.company.suppliers.first()
    supply = current_supplier.supplies.first()

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108')

    foreign_supplier = new_employee.company.suppliers.create(
        title='ForeignSupplier',
        INN='111111111111'
    )

    url = reverse('supply-edit', args=[supply.id])

    data = {
        'supplier': foreign_supplier.id,
        'delivery_date': '2026-03-01'
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

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Supply.objects.filter(id=supply.id).exists()

@pytest.mark.django_db
def test_delete_supply_employee_success(api_client, employee_with_supply):
    """Employee can delete a supply for their company"""

    api_client.force_authenticate(user=employee_with_supply)

    supplier = employee_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Supply.objects.filter(id=supply.id).exists()

@pytest.mark.django_db
def test_delete_supply_diff_employee_error(api_client, owner_with_supply):
    """Error: Employee of a different company cannot delete a supply"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108'
    )

    api_client.force_authenticate(new_employee)
    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_supply_unathorized_error(api_client, owner_with_supply):
    """Error: Unauthorized user cannot delete a supply"""

    supplier = owner_with_supply.company.suppliers.first()
    supply = supplier.supplies.first()

    url = reverse('supply-delete', args=[supply.id])
    response = api_client.delete(url)

    assert response.status_code == 401




