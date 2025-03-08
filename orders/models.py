# models.py
from django.db import models
from customers.models import Customer
from products.models import Product

# Model for Order
class Order(models.Model):
    # Order status choices
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4

    STATUS_CHOICE = (
        (CART_STAGE, 'CART_STAGE'),
        (ORDER_CONFIRMED, 'ORDER_CONFIRMED'),
        (ORDER_PROCESSED, 'ORDER_PROCESSED'),
        (ORDER_DELIVERED, 'ORDER_DELIVERED'),
        (ORDER_REJECTED, 'ORDER_REJECTED')
    )

    # Delete status choices
    ACTIVE = 1
    DELETED = 0
    DELETE_CHOICES = ((ACTIVE, 'Active'), (DELETED, 'Deleted'))

    order_status = models.IntegerField(choices=STATUS_CHOICE, default=CART_STAGE)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
    # Return the string of the human-readable status
        return self.get_order_status_display()
        
# Model for Ordered Item
class OrderedItem(models.Model):
    product = models.ForeignKey(Product, related_name='added_carts', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='added_items')

    def __str__(self):
        return '{} (Quantity: {})'.format(self.product.title, self.quantity)