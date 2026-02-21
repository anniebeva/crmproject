import pytest
from django.urls import reverse

from authenticate.models import User
from companies.models import Company
from .models import Storage
from utils import create_owner, create_employee


# Create storage POST

@pytest.mark.django_db
def test_create_storage_owner_success(api_client, owner_user):
    """Owner can create a storage for their company"""
    api_client.force_authenticate(user=owner_user)
    url = reverse('storage-create')
    data = {'address': 'Test_street 123, City 13092', 'company': owner_user.company.id}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_storage_employee_error(api_client, employee_user):
    """Error: Employee cannot create a storage"""

    api_client.force_authenticate(user=employee_user)
    url = reverse('storage-create')
    data = {'address': 'Test_street 123, City 13092', 'company': employee_user.company.id}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 403

@pytest.mark.django_db
def test_create_storage_unauthorized_error(api_client, owner_user):
    """Error: Unauthorized user cannot create a storage"""

    url = reverse('storage-create')
    data = {'address': 'Test_street 123, City 13092', 'company': owner_user.company.id}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401


@pytest.mark.django_db
def test_create_second_storage_error(api_client, owner_with_storage):
    """Error: Owner cannot create a second storage for the same company"""

    api_client.force_authenticate(user=owner_with_storage)

    url = reverse('storage-create')
    data = {'address': 'Second Street 2', 'company': owner_with_storage.company.id}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400

# View storage GET

@pytest.mark.django_db
def test_view_storage_owner_success(api_client, owner_with_storage):
    """Owner can view their company's storage"""

    api_client.force_authenticate(user=owner_with_storage)
    url = reverse('storage-detail', args=[owner_with_storage.company.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['company_id'] == owner_with_storage.company.id


@pytest.mark.django_db
def test_view_storage_employee_success(api_client, employee_with_storage):
    """Employee can view their company's storage"""

    api_client.force_authenticate(user=employee_with_storage)
    url = reverse('storage-detail', args=[employee_with_storage.company.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['company_id'] == employee_with_storage.company.id

@pytest.mark.django_db
def test_view_storage_diff_employee_error(api_client, owner_with_storage):
    """Error: employee of another company cannot view storage"""

    new_employee = create_employee(
        user_model=User,
        comp_model=Company,
        username='test_employee_storage',
        email='test_employee_storage@test.com',
        company_title='TestStorgeComp',
        inn='123456789106')

    api_client.force_authenticate(user=new_employee)

    url = reverse('storage-detail', args=[owner_with_storage.company.id])
    response = api_client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_view_storage_unauthorized_error(api_client, owner_with_storage):
    """Error: Unauthorized user cannot view storage"""

    url = reverse('storage-detail', args=[owner_with_storage.company.id])
    response = api_client.get(url)

    assert response.status_code == 401

# Edit storage PUT

@pytest.mark.django_db
def test_edit_storage_owner_success(api_client, owner_with_storage):
    """Owner can edit their company's storage"""

    api_client.force_authenticate(user=owner_with_storage)
    url = reverse('storage-edit', args=[owner_with_storage.company.id])
    new_data = {'address': 'New Street 123', 'company': owner_with_storage.company.id}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 200
    owner_with_storage.company.storage.refresh_from_db()
    assert owner_with_storage.company.storage.address == 'New Street 123'

@pytest.mark.django_db
def test_edit_storage_employee_error(api_client, employee_with_storage):
    """Error: employee cannot edit storage"""

    api_client.force_authenticate(user=employee_with_storage)
    url = reverse('storage-edit', args=[employee_with_storage.company.id])
    new_data = {'address': 'New_street 12, City 13092', 'company': employee_with_storage.company.id}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_storage_unauthorized_error(api_client, owner_with_storage):
    """Error: Unauthorized user cannot edit storage"""

    url = reverse('storage-edit', args=[owner_with_storage.company.id])
    new_data = {'address': 'New Street 456', 'company': owner_with_storage.company.id}
    response = api_client.put(url, new_data, format='json')

    assert response.status_code == 401


# Delete storage DELETE

@pytest.mark.django_db
def test_delete_storage_owner_success(api_client, owner_with_storage):
    """Owner can delete their company's storage"""

    api_client.force_authenticate(user=owner_with_storage)
    url = reverse('storage-delete', args=[owner_with_storage.company.id])
    response = api_client.delete(url)

    assert response.status_code == 204

    assert not Storage.objects.filter(company=owner_with_storage.company).exists()

@pytest.mark.django_db
def test_delete_storage_employee_error(api_client, employee_with_storage):
    """Error: employee tries to delete storage"""

    api_client.force_authenticate(user=employee_with_storage)
    url = reverse('storage-delete', args=[employee_with_storage.company.id])
    response = api_client.delete(url)

    assert  response.status_code == 403


@pytest.mark.django_db
def test_delete_storage_unauthorized_error(api_client, owner_with_storage):
    """Error: Unauthorized user cannot delete storage"""

    url = reverse('storage-delete', args=[owner_with_storage.company.id])
    response = api_client.delete(url)

    assert response.status_code == 401