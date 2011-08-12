from django import template

# Register all template tags/filters
register = template.Library()

@register.filter
def subtract(value, arg):
    """Subtract arg from value."""
    try:
        return int(value) - int(arg)
    except ValueError:
        try:
            return value + arg
        except TypeError:
            return ''

@register.filter
def absolute(value):
    """Get absolute value."""
    try:
        return abs(int(value))
    except ValueError:
        try:
            return abs(value)
        except TypeError:
            return ''

@register.filter
def dynamic_slice_left(sequence, left):
    """Slice function that allows variable as argument. It will return sequence[left:]."""
    try:
        return sequence[left:]
    except TypeError:
        return sequence

@register.filter
def dynamic_slice_right(sequence, right):
    """Slice function that allows variable as argument. It will return sequence[:right]."""
    try:
        return sequence[:right]
    except TypeError:
        return sequence
