from django.core.validators import validate_email
from rest_framework.serializers import ValidationError


def validate_forbidden_domains(value):
    """
        Расширенный валидатор, проверяющий отсутствие ссылок на сторонние ресурсы.
        Разрешает только YouTube и пустые значения.

        Запрещенные домены:
        - vk.ru
        - rutube.ru
        - dzen.ru
        - telegram.org
        """
    if not value:
        return value

    forbidden_domains = [
        'vk.ru',
        'rutube.ru',
        'dzen.ru',
        'telegram.org']

    allowed_domains = [
            'youtube.com'
        ]

    value_lower = value.lower()

    # Проверяем на запрещенные домены
    for domain in forbidden_domains:
        if domain in value_lower:
            raise ValidationError(
                (f'Использование ссылок на {domain} запрещено. Разрешены только YouTube ссылки.'),
                code='forbidden_domain'
            )

    # Проверяем, что ссылка ведет на YouTube
    is_youtube = False
    for domain in allowed_domains:
        if domain in value_lower:
            is_youtube = True
            break

    if not is_youtube:
        raise ValidationError(
            ('Разрешены только ссылки на YouTube (youtube.com)'),
            code='invalid_youtube_url'
        )

    return value
