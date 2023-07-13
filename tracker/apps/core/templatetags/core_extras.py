from django.utils import timezone
from django import template

register = template.Library()


def delta_format(td):
    """Given a time delta it returns a string

    The purpose of this function is to make a short delta string.
    If time delta is more than a day: only days amount to be returned
    If time delta is less than a day, and more than an hour: only hours amount to be returned
    If time delta is less than an hour: only minutes amount to be returned
    """

    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    remaining_hours = total_seconds % 86400
    remaining_minutes = remaining_hours % 3600
    hours = remaining_hours // 3600
    minutes = remaining_minutes // 60

    day_unit = "days" if days > 1 else "day"
    hour_unit = "hours" if hours > 1 else "hour"
    minute_unit = "minutes" if minutes > 1 else "minute"

    day_str = f"{days} {day_unit}" if days else ""
    hour_str = f"{hours} {hour_unit}" if (hours and not days) else ""
    minute_str = f"{minutes} {minute_unit}" if (minutes and not days and not hours) else ""

    return f"{day_str}{hour_str}{minute_str}"


@register.filter
def duration(td):
    return delta_format(td)


@register.filter
def custom_timesince(last_date):
    time_delta = timezone.now() - last_date
    return delta_format(time_delta)
