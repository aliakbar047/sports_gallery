from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .models import *
import json
import datetime



# Create your views here.

def home(request):
	
	products = Product.objects.all()
	if request.user.is_authenticated:
		customer = request.user
		try:
			order = Order.objects.get(customer=customer,ordered=False)
		except:
			order = {}
			print("hai how are you")
	else:
		order = {}
		
	context ={
		'products':products,
		'order':order
	}
	return render(request,'store/home.html',context)


def cart(request):
	if request.user.is_authenticated:
		customer = request.user
		items = customer.orderitem_set.all()
		try:
			order = Order.objects.get(customer=customer,ordered=False)
		except:
			order = {}
			print("hai how are you")
	else:
		order = {}
		items = {}
		
	context = {
		'items':items,
		'order':order
	}
	
	return render(request,'store/cart.html',context)


def checkout(request):
	if request.user.is_authenticated:
		customer = request.user
		items = customer.orderitem_set.all()
		try:
			order = Order.objects.get(customer=customer,ordered=False)
		except:
			order = {}
			print("hai how are you")
	else:
		order = {}
		items = {}
		
	context = {
		'items':items,
		'order':order
	}
	
	return render(request,'store/checkout.html',context)




def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

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

	orderItem.save()

	if not order.order_items.filter(id=orderItem.id).exists():
		order.order_items.add(orderItem)

	items = customer.orderitem_set.all()
	total_item = sum([item.quantity for item in items])
	total = sum([item.total for item in items])


	order.total_items = total_item
	order.total = total
	order.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
		order.order_items.remove(orderItem)


	return JsonResponse('Item was added', safe=False)



