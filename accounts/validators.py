import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(_('Şifre en az bir büyük harf içermelidir.'), code='password_no_upper')
        if not re.findall('[a-z]', password):
            raise ValidationError(_('Şifre en az bir küçük harf içermelidir.'), code='password_no_lower')
        if not re.findall('[0-9]', password):
            raise ValidationError(_('Şifre en az bir sayı içermelidir.'), code='password_no_digit')

    def get_help_text(self):
        return _('Şifreniz en az bir büyük harf, bir küçük harf ve bir sayı içermelidir.')