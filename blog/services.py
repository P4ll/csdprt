def get_userprofile(request):
    """ Получение профиля авторизованного пользователя """

    if request.user.is_authenticated:
        user = request.user
        return user
    else:
        return None