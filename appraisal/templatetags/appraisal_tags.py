from django import template

register = template.Library()

@register.filter(name='inr_currency')
def inr_currency(value):
    """
    Formats a numeric value using the Indian Numbering System grouping:
    Last 3 digits grouped, followed by comma-separated pairs of two digits (e.g., 12,50,000).
    """
    if value is None or value == '':
        return ''
    try:
        val = float(value)
        is_negative = val < 0
        val = abs(val)
        s = f"{val:.2f}"
        integer_part, decimal_part = s.split('.')

        if len(integer_part) <= 3:
            formatted_int = integer_part
        else:
            last3 = integer_part[-3:]
            rest = integer_part[:-3]
            groups = []
            while len(rest) > 2:
                groups.insert(0, rest[-2:])
                rest = rest[:-2]
            if rest:
                groups.insert(0, rest)
            formatted_int = ",".join(groups) + "," + last3

        prefix = "-" if is_negative else ""
        if decimal_part == '00':
            return f"{prefix}{formatted_int}"
        return f"{prefix}{formatted_int}.{decimal_part}"
    except (ValueError, TypeError):
        return value
