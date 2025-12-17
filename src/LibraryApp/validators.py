from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
import re

class ComplexPasswordValidator:
    """
    Validate that the password contains at least:
    - one uppercase letter
    - one lowercase letter
    - one digit
    - one special character
    """

    def validate(self, password, user=None):
        if len(password) < 10:
            raise ValidationError(
                _("Mật khẩu quá ngắn. Phải chứa ít nhất 10 ký tự."),
                code='password_too_short',
            )
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("Mật khẩu phải chứa ít nhất một chữ cái in hoa."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("Mật khẩu phải chứa ít nhất một chữ cái thường."),
                code='password_no_lower',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("Mật khẩu phải chứa ít nhất một chữ số."),
                code='password_no_digit',
            )
        if not re.findall('[^A-Za-z0-9]', password):
            raise ValidationError(
                _("Mật khẩu phải chứa ít nhất một ký tự đặc biệt (@, #, $, ...)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Mật khẩu phải chứa ít nhất 10 ký tự, bao gồm chữ cái in hoa, chữ cái thường, "
            "chữ số và ký tự đặc biệt."
        )
