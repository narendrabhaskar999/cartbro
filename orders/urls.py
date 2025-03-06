from . import views
from django.urls import path

urlpatterns = [
    path('cart/',views.show_cart,name='cart')
]
