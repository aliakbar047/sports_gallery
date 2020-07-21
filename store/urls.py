from django.urls import path

from .views import *


urlpatterns =[
    path('',home, name = 'home'),
    path('details/<int:pk>', productDetails, name = "details"),
    path('cart/', cart, name = "cart"),
    path('checkout/', checkout, name = "checkout"),
    path('profile/', customerProfile , name = 'profile'),
    path('wishlist/', savedItems, name = 'wishlist'),

    path('update_item/', updateItem, name = "update_item"),
    path('add_wishlist/', addWishlist, name= 'add_wishlist')
]