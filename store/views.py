from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import *
from .forms import AddressForm
from .utils import *
import json




# Create your views here.

def home(request):

	data = customerProduct(request)
	
	return render(request,'store/home.html',data)

def productDetails(request,pk):

	data = customerProduct(request)
	order = data['order']
	save_items = data['save_items']
	product = get_object_or_404(Product ,id=pk )
		
	context ={
		'product':product,
		'order':order,
		'save_items':save_items
	}
	return render(request,'store/details.html',context)


@login_required
def cart(request):

	data = customerProduct(request)
	
	return render(request,'store/cart.html',data)


def checkout(request):

	data = customerProduct(request)
	order = data['order']
	save_items = data['save_items']

	customer = request.user

	form = AddressForm(request.POST or None)
	if form.is_valid():
		address, created = Address.objects.get_or_create(customer=customer)
		address.name = form.cleaned_data.get('name')
		address.mobile = form.cleaned_data.get('phone_no')
		address.address1 = form.cleaned_data.get('address_1')
		address.address2 = form.cleaned_data.get('address_2')
		address.state = form.cleaned_data.get('state')
		address.city = form.cleaned_data.get('city')
		address.zip = form.cleaned_data.get('zip_code')
		save_for = form.cleaned_data.get('save_for_later')
		if save_for :
			address.save_for_later = save_for
		
		address.save()
		
		order.address = address
		order.ordered = True
		order.ordered_date = timezone.now()
		order.transaction_id = timezone.now().timestamp()
		
		for item in order.order_items.all():
			item.complete = True
			item.save()
			
		order.save()
		
		return redirect('/profile/')

		
	context = {
		'order':order,
		'save_items':save_items,
		'form':form
	}
	
	return render(request,'store/checkout.html',context)


def customerProfile(request):

	data = customerProduct(request)
	order = data['order']
	save_items = data['save_items']

	customer = request.user
	try:
		ordered = Order.objects.filter(customer=customer,ordered=True).order_by('-id')
	except:
		ordered = ''

	context = {
		'ordered':ordered,
		'order':order,
		'save_items':save_items
	}
	
	return render(request,'store/profile.html',context)

	

@login_required
def updateItem(request):

	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	
	customer = request.user
	product = Product.objects.get(id=productId)
	
	orderItem, created = OrderItem.objects.get_or_create(
		customer=customer, 
		product=product,
		complete=False
	)

	order, created = Order.objects.get_or_create(customer=customer, ordered=False)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
		orderItem.total = (orderItem.quantity * product.price)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
		orderItem.total = (orderItem.quantity * product.price)

	elif action == 'delete':
		orderItem.quantity = 0
		orderItem.total = 0
		
	orderItem.save()

	if not order.order_items.filter(id=orderItem.id).exists():
		order.order_items.add(orderItem)

	items = customer.orderitem_set.filter(complete=False)
	total_item = sum([item.quantity for item in items])
	total = sum([item.total for item in items])


	order.total_items = total_item
	order.total = total
	order.save()
		
		

	if orderItem.quantity <= 0:
		orderItem.delete()
		order.order_items.remove(orderItem)
		
		
	if order.total_items <= 0:
		order.delete()


	return JsonResponse('Item was added', safe=False)


def addWishlist(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']

	
	customer = request.user
	product = Product.objects.get(id=productId)

	try:
		wishlist = WishList.objects.get(customer=customer, product=product)
		
	except:
		WishList.objects.create(
			customer=customer, product=product)
	else:
		if action != 'add':
			wishlist.delete()


	return JsonResponse('successfully added', safe=False)

@login_required
def savedItems(request):

	data = customerProduct(request)
	
	return render(request, 'store/wishlist.html' ,data)




	





