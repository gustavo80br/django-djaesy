import pandas

from djaesy.templatetags.app_panel import duration


def boolean_column(inverse=False, use_red=False):
    def bool_col(value, row, column_id, request):
        value = bool(not value) if inverse else value
        if value:
            icon = 'mdi-check-circle green-text'
        else:
            if use_red:
                icon = 'mdi-close-circle red-text'
            else:
                icon = 'mdi-minus-circle grey-text'
        return f'<i class="mdi {icon}"></i>'
    return bool_col


def datetime_column(date_format='%d/%m/%Y %H:%M'):

    def datetime_col(value, row, column_id, request):
        if pandas.isnull(value):
            return ' - '
        else:
            return value.strftime(date_format)

    return datetime_col


def duration_column(value, row, column_id, request):
    if pandas.isnull(value):
        return ' - '
    else:
        return duration(value)


def decimal_column(decimals=2, digit_separator=',', thousand_separator='.', postfix=''):
    def decimal_col(value, row, column_id, request):
        val = f'{round(value, decimals):,}{postfix}'
        maketrans = val.maketrans
        val = val.translate(maketrans(',.', '.,'))
        return val
    return decimal_col


