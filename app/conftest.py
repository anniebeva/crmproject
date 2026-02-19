from rest_framework.test import APIClient
import pytest
from authenticate.models import User
from companies.models import Company
from storage.models import Storage
from utils import create_employee, create_owner

#Fixtures
@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    """Clean test user not attached to any company"""
    test_user = User.objects.create_user(username='test_user',
                                         email='test_user@test.com',
                                         password='123456789101')
    return test_user


@pytest.fixture
def owner_user(db):
    """Test company owner"""

    owner = create_owner(user_model=User,
                         comp_model=Company,
                         username='test_owner',
                         email='test_owner@test.com',
                         company_title='TestOwnerCompany',
                         inn='123456789102')
    return owner

@pytest.fixture
def employee_user(db):
    """Test employee attached to a company"""
    employee = create_employee(user_model=User,
                               comp_model=Company,
                               username='test_employee',
                               email='test_employee@test.com',
                               company_title='TestEmployeeCompany',
                               inn='1234567891013')
    return employee


@pytest.fixture
def owner_with_storage(owner_user):
    """Create storage for test owner"""

    Storage.objects.create(
        company=owner_user.company,
        address='Test_street 123, City 13092'
    )
    return owner_user


@pytest.fixture
def employee_with_storage(employee_user):
    """Create storage for test employee"""

    Storage.objects.create(
        company=employee_user.company,
        address='Empl_street 123, City 13092'
    )
    return employee_user