from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderedItem
from products.models import Product
from django.contrib import messages

# Ensure user has a customer profile before proceeding
def get_customer(user):
    return getattr(user, 'customer_profile', None)


def show_cart(request):
    user=request.user
    customer=get_customer(user)

    if not customer:
        messages.error(request, "You need a customer profile to access the cart.")
        return redirect('home') # Redirect to home or prpfile creation

    cart_obj=Order.objects.filter(
        owner=customer,
        order_status=Order.CART_STAGE
        ).first() # Ensures only one cart is used
    
    context={'cart':cart_obj}
    return render(request, 'cart.html',context)

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = get_customer(user)

        # Ensure user has a customer profile
        if not customer:
            messages.error(request, "You need a customer profile to add items to cart.")
            return redirect('cart')
 
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        

        # Get or create an active cart for the customer
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Check if the item already exists in the cart
        ordered_item, item_created = OrderedItem.objects.get_or_create(
            product=product,
            owner=cart_obj
        )

        # If item exists, update quantity instead of creating duplicate entries
        if not item_created:
            ordered_item.quantity += quantity
            ordered_item.save()
            messages.success(request, "Added " + str(quantity) + "x " + product.title + " to cart.")
        
        return redirect('cart')
    
    # Handle GET requests gracefully
    messages.error(request, "Invalid request method.")
    return redirect('cart')

def remove_item_from_cart(request,pk):
    item=OrderedItem.objects.get(pk=pk)
    if item:
        item.delete()
        messages.success(request,"Item removed from cart.")
    return redirect('cart')

def checkout_cart(request):
    if request.method == 'POST':
        user = request.user
        customer = get_customer(user)

        if not customer:
            messages.error(request, "You need a customer profile to checkout.")
            return redirect('cart')
        
        total = float(request.POST.get('total'))

        # Debugging check
        print("Order type:", type(Order))  # Ensure Order is not an int

        # Ensure we get a QuerySet
        order_obj = Order.objects.filter(owner=customer, order_status=Order.CART_STAGE).first()

        if order_obj:
            order_obj.order_status = Order.ORDER_CONFIRMED
            order_obj.save()
            messages.success(request, "Your order is processed. Your item will be delivered in two days.")
        else:
            messages.error(request, "Unable to process. No items in cart.")

    return redirect('cart')



def view_orders(request):
    user=request.user
    customer=get_customer(user)

    if not customer:
            messages.error(request, "You need a customer profile to checkout.")
            return redirect('cart')
   
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    return render(request,'orders.html',context)






