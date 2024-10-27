def is_employee(user):
    """Checks that the given user has the group employee"""
    return user.groups.filter(name='Mitarbeiter').exists()