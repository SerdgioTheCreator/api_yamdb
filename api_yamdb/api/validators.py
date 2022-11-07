from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    def __call__(self, value):
        regex_matches = self.regex.search(str(value))
        invalid_input = (regex_matches if self.inverse_match
                         else not regex_matches)
        if invalid_input:
            raise ValidationError(
                self.message,
                code=self.code,
                params={'value': value}
            )
        if value == 'me':
            raise ValidationError('Имя пользователя "me" недоступно.')
