import re
from django.core.exceptions import ValidationError


def validate_username(value):
    regex = re.compile(r'^[\w.@+-]+\Z')
    regex_matches = re.search(regex, str(value))
    if not regex_matches:
        pattern = re.compile(r'[\w.@+-]')
        unmatched = re.sub(pattern, '', str(value))
        raise ValidationError(
            'Введите корректное имя пользователя.'
            'Оно может содержать только буквы и символы @/./+/-/_. '
            f'Обнаружены недопустимые символы: {unmatched}'
        )
    if value == 'me':
        raise ValidationError('Имя пользователя "me" недоступно.')
