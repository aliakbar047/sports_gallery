from .models import *

def customerProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        try :
            order = Order.objects.get(customer=customer,ordered=False)
        except:
            order = ''
        wishlist = customer.wishlist_set.all()
        if wishlist :
            save_items = len(wishlist)
        else:
            wishlist = ''
            save_items = 0
            
    else:
        order = ''
        wishlist = ''
        save_items = 0

    products = Product.objects.all()

    return {'order':order ,'wishlist':wishlist, 'save_items':save_items, 'products':products}



	
