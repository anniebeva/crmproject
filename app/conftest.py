from rest_framework.test import APIClient
import pytest
import datetime

from authenticate.models import User
from companies.models import Company
from storage.models import Storage
from suppliers.models import Supplier
from supplies.models import Supply
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

@pytest.fixture
def owner_with_supplier(owner_user):
    """create supplier for test owner"""

    Supplier.objects.create(
        company=owner_user.company,
        title='TestSupplier1',
        INN='999999999999'
    )

    return owner_user


@pytest.fixture
def employee_with_supplier(employee_user):
    """create supplier for test employee"""

    Supplier.objects.create(
        company=employee_user.company,
        title='TestSupplier1',
        INN='999999999999'
    )

    return employee_user


@pytest.fixture
def owner_with_supply(owner_with_supplier):
    """create supply for test owner"""
    supplier = owner_with_supplier.company.suppliers.first()

    Supply.objects.create(
        supplier=supplier,
        delivery_date=datetime.date.today()
    )

    return owner_with_supplier


@pytest.fixture
def employee_with_supply(employee_with_supplier):
    """create supply for test employee"""
    supplier = employee_with_supplier.company.suppliers.first()

    Supply.objects.create(
        supplier=supplier,
        delivery_date=datetime.date.today()
    )

    return employee_with_supplier