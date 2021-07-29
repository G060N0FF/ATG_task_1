from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


# check for alphanumeric passwords
class AlphanumericPasswordValidator:
    def validate(self, password, user=None):
        if not password.isalnum():
            raise ValidationError(
                _("This password must be alphanumeric."),
                code='password_not_alphanumeric',
            )

    def get_help_text(self):
        return _(
            "Your password must be alphanumeric."
        )
