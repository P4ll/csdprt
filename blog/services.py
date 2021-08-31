def get_userprofile(request):
    """ Получение профиля авторизованного пользователя """

    if request.user.is_authenticated:
        user = request.user
        return user
    else:
        return None


def get_change_color_text(title, text):
    """Меняем цвет словосочетаний в тексте, которые совпадают с заголовком"""
    text = text.replace(title, f'<span class="custom-text-for-news">{title}</span>')
    return text
