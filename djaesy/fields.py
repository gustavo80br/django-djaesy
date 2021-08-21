from django.forms.fields import DateTimeField
from django.utils.translation import gettext_lazy as _
import re

from django.core.validators import RegexValidator
from django.db.models import CharField

from djaesy.widgets import DateRangePicker

postal_code_re = re.compile(r'^(\d{5}-\d{3})|(\d{8})$')


class BRPostalCodeValidator(RegexValidator):
    """
    A validator for Brazilian Postal Codes (CEP).

    .. versionadded:: 2.2
    """

    def __init__(self, *args, **kwargs):
        self.message = _('Enter a postal code in the format 00000-000.')
        self.code = _('Invalid Postal Code')
        super(BRPostalCodeValidator, self).__init__(postal_code_re, *args, **kwargs)


class BRPostalCodeField(CharField):
    """
    A model field for the brazilian zip code

    .. versionadded:: 2.2
    """

    description = _("Postal Code")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9
        super(BRPostalCodeField, self).__init__(*args, **kwargs)
        self.validators.append(BRPostalCodeValidator())


class DateRangePickerField(DateTimeField):
    widget = DateRangePicker

    def __init__(self, *, drop=None, **kwargs):
        widget = kwargs.get('widget', None)
        if drop and not widget:
            kwargs['widget'] = DateRangePicker(attrs={'data-drops': drop})
        super().__init__(**kwargs)

    def to_python(self, value):
        dates = value.split(' - ')
        result = []
        for date in dates:
            d = super().to_python(date)
            if d:
                result.append(d)
        return result
