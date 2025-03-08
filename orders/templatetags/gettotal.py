from django import template

register = template.Library()

@register.simple_tag(name='gettotal')  # Fix typo here
def gettotal(cart):
    total = sum(item.quantity * item.product.price for item in cart.added_items.all())
    return total
