import pytest
from django.urls import reverse

from authenticate.models import User
from companies.models import Company
from .models import Supplier
from utils import create_owner, create_employee


#Create POST

@pytest.mark.django_db
def test_create_supplier_owner_success(api_client, owner_user):
    """Owner can create a supplier for their company"""

    api_client.force_authenticate(user=owner_user)
    url = reverse('supplier-create')
    data = {'company': owner_user.company.id,
            'title': 'OwnerSupplierTest',
            'INN': '888888888888'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

@pytest.mark.django_db
def test_create_supplier_employee_success(api_client, employee_user):
    """Employee can create a supplier for their company"""

    api_client.force_authenticate(user=employee_user)
    url=reverse('supplier-create')
    data = {'company': employee_user.company.id,
            'title': 'EmployeeSupplierTest',
            'INN': '888888888889'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201

@pytest.mark.django_db
def test_create_supplier_diff_employee_error(api_client, owner_with_supplier):
    """Error: Employee of a different company cannot create a supplier"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789108')

    api_client.force_authenticate(user=new_employee)

    url = reverse('supplier-create')
    data = {'company': owner_with_supplier.company.id,
        'title': 'EmployeeSupplierTest',
        'INN': '888888888889'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 403

@pytest.mark.django_db
def test_create_supplier_unathorized_error(api_client, owner_user):
    """Error: Unauthorized user cannot create a supplier"""

    url = reverse('supplier-create')
    data = {'company': owner_user.company.id,
            'title': 'OwnerSupplierTest',
            'INN': '888888888888'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401

#View supplier GET

@pytest.mark.django_db
def test_view_supplier_owner_success(api_client, owner_with_supplier):
    """Owner can view suppliers for their company"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()
    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supplier.id
    assert response.data['company_id'] == owner_with_supplier.company.id


@pytest.mark.django_db
def test_view_supplier_employee_success(api_client, employee_with_supplier):
    """Owner can view suppliers for their company"""

    api_client.force_authenticate(user=employee_with_supplier)
    supplier = employee_with_supplier.company.suppliers.first()
    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == supplier.id
    assert response.data['company_id'] == employee_with_supplier.company.id

@pytest.mark.django_db
def test_view_supplier_diff_employee_error(api_client, owner_with_supplier):
    """Error: employee of another company cannot view supplier detail"""

    supplier = owner_with_supplier.company.suppliers.first()

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='other_emp',
        email='other_emp@test.com',
        company_title='OtherCompany',
        inn='987654321001'
    )

    api_client.force_authenticate(user=new_employee)

    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 403

@pytest.mark.django_db
def test_view_supplier_unathorized_error(api_client, owner_with_supplier):
    """Error: unathorized users cannot access suppliers"""

    supplier = owner_with_supplier.company.suppliers.first()
    url = reverse('supplier-detail', args=[supplier.id])
    response = api_client.get(url)

    assert response.status_code == 401


#Edit supplier PUT

@pytest.mark.django_db
def test_edit_supplier_owner_success(api_client, owner_with_supplier):
    """Owner can edit their company's supplier"""

    api_client.force_authenticate(user=owner_with_supplier)
    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supplier-edit', args=[supplier.id])
    new_data ={'company': owner_with_supplier.company.id,
               'title': 'SupplierUpdateOwnerTest',
               'INN': '888888888888'}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 200

    supplier.refresh_from_db()
    assert supplier.INN == '888888888888'

@pytest.mark.django_db
def test_edit_supplier_employee_success(api_client, employee_with_supplier):
    """Employee can edit their company's supplier"""

    api_client.force_authenticate(user=employee_with_supplier)
    supplier = employee_with_supplier.company.suppliers.first()

    url = reverse('supplier-edit', args=[supplier.id])
    new_data = {'company': employee_with_supplier.company.id,
                'title': 'SupplierUpdateOwnerTest',
                'INN': '888888888888'}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 200

    supplier.refresh_from_db()
    assert supplier.INN == '888888888888'

@pytest.mark.django_db
def test_edit_supplier_diff_employee_error(api_client, owner_with_supplier):
    """Error: employee of another company cannot edit supplier detail"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_supplier',
        email='test_employee_supplier@test.com',
        company_title='TestSupplierComp',
        inn='123456789106')

    api_client.force_authenticate(user=new_employee)

    supplier = owner_with_supplier.company.suppliers.first()
    url = reverse('supplier-edit', args=[supplier.id])

    new_data = {'company': owner_with_supplier.company.id,
                'title': 'SupplierUpdateOwnerTest',
                'INN': '888888888888'}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_supplier_unathorized_error(api_client, owner_with_supplier):
    """Error: unathorized users cannot edit suppliers"""

    supplier = owner_with_supplier.company.suppliers.first()
    url = reverse('supplier-edit', args=[supplier.id])

    new_data = {'company': owner_with_supplier.company.id,
                'title': 'SupplierUpdateOwnerTest',
                'INN': '888888888888'}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 401


#Delete supplier DELETE

@pytest.mark.django_db
def test_delete_supplier_owner_success(api_client, owner_with_supplier):
    """Owner can delete their company's supplier"""

    api_client.force_authenticate(user=owner_with_supplier)

    supplier = owner_with_supplier.company.suppliers.first()
    url = reverse('supplier-delete', args=[supplier.id])

    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Supplier.objects.filter(id=supplier.id).exists()

@pytest.mark.django_db
def test_delete_supplier_employee_success(api_client, employee_with_supplier):
    """Employee can delete their company's supplier"""

    api_client.force_authenticate(user=employee_with_supplier)

    supplier = employee_with_supplier.company.suppliers.first()
    url = reverse('supplier-delete', args=[supplier.id])

    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Supplier.objects.filter(id=supplier.id).exists()

@pytest.mark.django_db
def test_delete_supplier_diff_employee_error(api_client, owner_with_supplier):
    """Error: Employee of another company cannot delete supplier"""

    supplier = owner_with_supplier.company.suppliers.first()

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='other_emp',
        email='other_emp@test.com',
        company_title='OtherCompany',
        inn='987654321001'
    )

    api_client.force_authenticate(user=new_employee)

    url = reverse('supplier-delete', args=[supplier.id])
    response = api_client.delete(url)

    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_supplier_unathorized_error(api_client, owner_with_supplier):
    """Error: Unauthorized user cannot delete supplier"""

    supplier = owner_with_supplier.company.suppliers.first()

    url = reverse('supplier-delete', args=[supplier.id])
    response = api_client.delete(url)

    assert response.status_code == 401