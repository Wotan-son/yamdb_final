from django.core.exceptions import ValidationError
from django.utils import timezone


def check_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            ('Вы указали год %(value)s больше текущего.'),
            params={'value': value},
        )
    if value < 0:
        raise ValidationError(
            'Год может быть только положительным числом.'
        )
