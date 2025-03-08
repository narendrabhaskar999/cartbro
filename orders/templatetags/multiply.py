from django import template

register = template.Library()

# Multiply filter
@register.simple_tag(name='multiply')
def multiply(a, b):
        # Multiplies value by arg.
    try:
        return a*b
    except (TypeError, ValueError):
        return 0  # Return 0 if there's an error with the multiplication

