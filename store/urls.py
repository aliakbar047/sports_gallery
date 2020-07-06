from django.urls import path

from .views import *


urlpatterns =[
    path('',home, name='home'),
    path('cart/', cart, name="cart"),

    path('update_item/', updateItem, name="update_item"),
]