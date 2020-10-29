from django import template


register = template.Library()


@register.filter
def duration(td):

    total_seconds = int(td.total_seconds())

    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60
    seconds = remaining_minutes % 60

    days_str = f'{days}d ' if days else ''
    hours_str = f'{str(hours).zfill(2)}:' if hours else '00:'
    minutes_str = f'{str(minutes).zfill(2)}' if minutes else '00'
    seconds_str = f':{str(seconds).zfill(2)}' if seconds else ':00'

    return f'{days_str}{hours_str}{minutes_str}{seconds_str}'
