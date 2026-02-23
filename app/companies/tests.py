from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from authenticate.models import User
from companies.models import Company

#Create company tests POST

@pytest.mark.django_db
def test_create_company_success(api_client, test_user):
    """Create company by an unattached user"""
    api_client.force_authenticate(user=test_user)
    url = reverse('company-create')
    data = {'title': 'NewCompany', 'INN': '098765432101'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['title'] == 'NewCompany'

@pytest.mark.django_db
def test_create_company_owner_error(api_client, owner_user):
    """Error: owner trying yto create another company"""

    api_client.force_authenticate(user=owner_user)
    url = reverse('company-create')
    data = {'title': 'TestCompany', 'INN': '222333444555'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_create_company_employee_error(api_client, employee_user):
    """Error: employee tries to create a company"""

    api_client.force_authenticate(user=employee_user)
    url = reverse('company-create')
    data = {'title': 'TestCompany', 'INN': '333444555666'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_create_company_unauthorized_error(api_client):
    """Error: unathorized user tries to  create a company"""

    url = reverse('company-create')
    data = {'title': 'FailCompany', 'INN': '444555666777'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 401


#View company. GET

@pytest.mark.django_db
def test_view_company_owner_success(api_client, owner_user):
    """View company detail by owner"""

    api_client.force_authenticate(user=owner_user)
    url = reverse('company-detail', args=[owner_user.company.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['title'] == owner_user.company.title

@pytest.mark.django_db
def test_view_company_employee_success(api_client, employee_user):
    """View company detail by employee"""

    api_client.force_authenticate(user=employee_user)
    url = reverse('company-detail', args=[employee_user.company.id])
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['title'] == employee_user.company.title

@pytest.mark.django_db
def test_view_company_unauthorized_error(api_client, owner_user):
    """Error: unathorized user tries to  create a company"""

    url = reverse('company-detail', args=[owner_user.company.id])
    response = api_client.get(url)

    assert response.status_code == 401

#Edit tests PUT

@pytest.mark.django_db
def test_edit_company_owner_success(api_client, owner_user):
    """Edit company detail by owner"""

    api_client.force_authenticate(user=owner_user)
    url = reverse('company-edit', args=[owner_user.company.id])
    data = {'title': 'UpdatedCompany', 'INN': '111111111111'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 200

    owner_user.company.refresh_from_db()
    assert owner_user.company.title == 'UpdatedCompany'


@pytest.mark.django_db
def test_edit_company_employee_error(api_client, employee_user):
    """Error: employee tries to edit company"""

    api_client.force_authenticate(user=employee_user)
    url = reverse('company-edit', args=[employee_user.company.id])
    data = {'title': 'FailEdit', 'INN': '111111111112'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_company_unauthorized_error(api_client, owner_user):
    """Error: unathorized user tries to edit company detail"""

    url = reverse('company-edit', args=[owner_user.company.id])
    data = {'title': 'FailEdit', 'INN': '111111111113'}
    response = api_client.put(url, data, format='json')

    assert response.status_code == 401


#Delete tests

@pytest.mark.django_db
def test_delete_company_owner_success(api_client, owner_user):
    """Test deleting company by owner"""

    api_client.force_authenticate(user=owner_user)
    url = reverse('company-delete', args=[owner_user.company.id])
    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Company.objects.filter(id=owner_user.company.id).exists()

@pytest.mark.django_db
def test_delete_company_employee_error(api_client, employee_user):
    """Error: employee tries to delete a company"""

    api_client.force_authenticate(user=employee_user)
    url = reverse('company-delete', args=[employee_user.company.id])
    response = api_client.delete(url)

    assert  response.status_code == 403


@pytest.mark.django_db
def test_delete_company_unauthorized_error(api_client, owner_user):
    """Error: unauthorized user tries to delete a company"""
    url = reverse('company-delete', args=[owner_user.company.id])
    response = api_client.delete(url)

    assert response.status_code == 401