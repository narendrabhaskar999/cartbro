from django import template

register = template.Library()

# Multiply filter
@register.filter(name='multiply')
def multiply(value, arg):
    """Multiplies value by arg."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Return 0 if there's an error with the multiplication

# Chunks filter (splits a list into chunks of a specified size)
@register.filter(name='chunks')
def chunks(list_data, chunk_size):
    chunk = []
    i = 0
    for data in list_data:
        chunk.append(data)
        i += 1
        if i == chunk_size:
            yield chunk
            i = 0
            chunk = []
    if chunk:
        yield chunk
