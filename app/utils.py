def create_owner(user_model, comp_model, username, email, company_title, inn):
    """Support function to create company owner with company"""

    user = user_model.objects.create_user(username=username, email=email, password='12345678')
    company = comp_model.objects.create(title=company_title, INN=inn)
    user.company = company
    user.is_company_owner = True
    user.save()

    return user

def create_employee(user_model, comp_model, username, email, company_title, inn):
    """Support function to create employee"""

    user = user_model.objects.create_user(username=username, email=email, password='12345678')
    company = comp_model.objects.create(title=company_title, INN=inn)
    user.company = company
    user.is_company_owner = False
    user.save()

    return user