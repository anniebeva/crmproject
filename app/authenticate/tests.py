from rest_framework.test import APIClient
import pytest
from django.urls import reverse
from authenticate.models import User
from companies.models import Company
from utils import create_owner, create_employee


@pytest.mark.django_db
def test_create_new_user(api_client):
    """Create new user"""

    url = reverse('register')
    data = {'username': 'test_user1',
             'email': 'test_user1@test.com',
            'password': '12345678'}
    response = api_client.post(url, data, format='json')

    assert response.status_code == 201
    assert response.data['email'] == 'test_user1@test.com'


# Attach user to company tests

@pytest.mark.django_db
def test_attach_user_to_company_success(api_client, owner_user):
    """Attach new user to company"""

    api_client.force_authenticate(user=owner_user)

    new_user = User.objects.create_user(username='test_user2',
                                        email='test_user2@test.com',
                                        password="12345678")
    url = reverse('attach-user-to-company')
    response = api_client.post(url, {'email': new_user.email}, format='json')

    assert response.status_code == 200
    new_user.refresh_from_db()
    assert new_user.company == owner_user.company


@pytest.mark.django_db
def test_attach_user_to_company_access_error(api_client, employee_user):
    """Error: mployee cannot attach new user to company"""

    api_client.force_authenticate(user=employee_user)

    new_user = User.objects.create_user(username='test_user3',
                                        email='test_user3@test.com',
                                        password='12345678')
    url = reverse('attach-user-to-company')
    response = api_client.post(url, {'email': new_user.email}, format='json')

    assert response.status_code == 403

@pytest.mark.django_db
def test_attach_user_w_company_to_company_error(api_client, owner_user, employee_user):
    """Error: owner tries to attach employee of another company"""

    api_client.force_authenticate(user=owner_user)

    url = reverse('attach-user-to-company')
    response = api_client.post(url, {'email': employee_user.email}, format='json')

    assert response.status_code == 400


@pytest.mark.django_db
def test_attach_user_w_company_to_company_error_new_owner(api_client, owner_user):
    """Error: owner tries to attach another owner (already attached to company)"""
    api_client.force_authenticate(user=owner_user)

    new_owner = create_owner(
        user_model=User,
        comp_model=Company,
        username='test_owner2',
        email='test_owner2@test.com',
        company_title='TestOwnerCompany2',
        inn='123456789103')

    url = reverse('attach-user-to-company')
    response = api_client.post(url, {'email': new_owner.email}, format='json')

    assert response.status_code == 400

@pytest.mark.django_db
def test_no_user_error(api_client, owner_user):
    """Error: user doesn't exist"""
    api_client.force_authenticate(user=owner_user)

    url = reverse('attach-user-to-company')
    response = api_client.post(url, {'email': 'nonexistent@test.com'}, format='json')

    assert response.status_code == 404

