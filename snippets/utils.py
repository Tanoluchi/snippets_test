def is_the_owner(request, owner):
    """ Verifies if the current user is the owner of the snippet """
    return request.user.username == owner