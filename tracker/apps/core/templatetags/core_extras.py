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

    days_str = f"{days} days, " if days else ""
    hours_str = f"{hours} h" if hours else ""
    minutes_str = f"{minutes} m" if not hours else ""

    return f"{days_str}{hours_str}{minutes_str}"
