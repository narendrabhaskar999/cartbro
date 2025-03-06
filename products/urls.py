from .import views
from django.urls import path

urlpatterns = [
    path('home/',views.index,name="home"),
    path('product_list/',views.list_products,name='list_product'),
    path('product_detail/<pk>',views.detail_product,name='detail_product'),
     
]



 