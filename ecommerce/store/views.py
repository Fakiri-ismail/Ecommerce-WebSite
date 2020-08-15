from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.forms import modelformset_factory
from django.core.paginator import Paginator

from .models import Product,Order,OrderItem,ShippingAddress, Category, ProductImage, Contact
from .utils import cartData, guestOrder, cartItems
from .forms import ProductForm
from .filters import ProductFilter

import json
import datetime

def home(request):
	data = cartData(request)
	cartItems = data['cartItems']

	products= []
	products.append(Product.objects.get(id=96))
	products.append(Product.objects.get(id=60))
	products.append(Product.objects.get(id=94))
	products.append(Product.objects.get(id=112))

	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'pages/home.html', context)

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.filter(is_hide=False)

	productFilter=ProductFilter(request.GET, queryset=products)
	products = productFilter.qs

	paginator = Paginator(products, 16)
	page_num = request.GET.get('page')
	products_page = paginator.get_page(page_num)

	context = {'products':products,'productFilter':productFilter, 'products_page':products_page, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

@login_required(login_url="/login/")
def myStore(request):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_seller:
		products=Product.objects.filter(creator=request.user,is_hide=False)

		paginator = Paginator(products, 12)
		page_num = request.GET.get('page')
		products_page = paginator.get_page(page_num)

		context = {'products_page':products_page, 'cartItems':cartItems}
		return render(request, 'store/myStore.html', context)

	raise Http404()

@login_required(login_url="/login/")
def archProducts(request):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_seller:
		products=Product.objects.filter(creator=request.user,is_hide=True)
		paginator = Paginator(products, 12)
		page_num = request.GET.get('page')
		products_page = paginator.get_page(page_num)

		context = {'products_page':products_page, 'cartItems':cartItems}
		return render(request, 'store/product/archProducts.html', context)

	raise Http404()

def product_details(request, id):
	data = cartData(request)
	cartItems = data['cartItems']

	product = get_object_or_404(Product, id=id)

	context = {'product':product, 'cartItems':cartItems}
	return render(request, 'store/product/product_details.html', context)

@login_required(login_url="/login/")
def addProduct(request):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_seller:
		ImageForm = modelformset_factory(ProductImage, fields=('image',),extra=4)
		if request.method=='POST':
			form = ProductForm(request.POST)
			formImg = ImageForm(request.POST or None, request.FILES or None)
			if form.is_valid() and formImg.is_valid():
				product = form.save(commit=False)
				product.creator = request.user
				product.save()

				for img in formImg:
					if img.cleaned_data != {}:
						try:
							photo = ProductImage(product=product, image=img.cleaned_data.get('image'))
							photo.save()
						except Exception as e:
							break

				form = ProductForm()
				formImg = ImageForm(queryset=ProductImage.objects.none())
				succ = 'successfully added'
				context = {'form':form, 'formImg':formImg, 'succ':succ,'cartItems':cartItems}

				return render(request, 'store/product/addProduct.html', context)

		form = ProductForm()
		formImg = ImageForm(queryset=ProductImage.objects.none())
		context = {'form':form, 'formImg':formImg,'cartItems':cartItems}
		return render(request, 'store/product/addProduct.html', context)
	
	raise Http404()

@login_required(login_url="/login/")
def updatePrudact(request,id):
	data = cartData(request)
	cartItems = data['cartItems']
	
	if request.user.is_seller:
		product= get_object_or_404(Product, id=id)
		ImageForm = modelformset_factory(ProductImage, fields=('image',),extra=4, max_num=4)
		if product.creator != request.user:
			raise Http404()
		if request.method=='POST':
			form = ProductForm(request.POST or None, instance=product)
			formImg = ImageForm(request.POST or None, request.FILES or None)
			if form.is_valid() and formImg.is_valid():
				form.save()

				print('-----------------------------------------')
				print(formImg.cleaned_data)
				print('-----------------------------------------')

				images=ProductImage.objects.filter(product=product)
				for index, img in enumerate(formImg):
					if img.cleaned_data:
						# New photo is added
						if img.cleaned_data.get('id') is None:
							photo = ProductImage(product=product, image=img.cleaned_data.get('image'))
							photo.save()
						# Delete photo allredy exist
						elif img.cleaned_data.get('image') is False:
							photo = ProductImage.objects.get(id=request.POST.get('form-'+str(index)+'-id'))
							photo.delete()
						# Update photo allredy exist and delete the old photo	
						else:
							photo = ProductImage(product=product, image=img.cleaned_data.get('image'))
							d = ProductImage.objects.get(id=images[index].id)
							if photo.imageURL != d.imageURL:
								d.image.delete(save=False)
							d.image = photo.image
							d.save()

				return myStore(request)

		form = ProductForm(instance=product)
		formImg = ImageForm(queryset=ProductImage.objects.filter(product=product))

		context = {'form':form, 'formImg':formImg,'cartItems':cartItems}
		return render(request, 'store/product/updatePrudact.html', context)
	
	raise Http404()

@login_required(login_url="/login/")
def deleteProduct(request,id):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.user.is_seller:
		product= get_object_or_404(Product, id=id)
		if product.creator != request.user:
			raise Http404()

		if request.method=='POST':
			product.delete()
			products=Product.objects.filter(creator=request.user)
			context = {'products':products,'cartItems':cartItems}

			return render(request, 'store/myStore.html', context)

		context = {'product':product,'cartItems':cartItems}
		return render(request, 'store/product/deleteProduct.html', context)

	raise Http404()

@login_required(login_url="/login/")
def archivePrudact(request,id):
	product= get_object_or_404(Product, id=id)
	if request.user.is_seller and product.creator == request.user:
		if product.is_hide:
			product.is_hide=False
		else:
			product.is_hide=True
		product.save()
		return archProducts(request)

	raise Http404()

	
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	for itm in order.orderitem_set.all():
		print(itm.product.title +"  "+str(itm.quantity))
		product = Product.objects.get(id=itm.product.id)
		product.quantity = product.quantity - itm.quantity
		if product.quantity <=0:
			product.delete()
		else:
			product.save()
	
	ShippingAddress.objects.create(
	customer=customer,
	order=order,
	address=data['shipping']['address'],
	city=data['shipping']['city'],
	state=data['shipping']['state'],
	zipcode=data['shipping']['zipcode'],
	)

	return JsonResponse('Payment submitted..', safe=False)

def contact(request):
	data = cartData(request)
	cartItems = data['cartItems']

	if request.method=='POST':
		if request.user.is_authenticated:
			email = request.user.email
		else:
			email = request.POST['email']
		msg = request.POST['message']
		contact = Contact(email=email, message=msg)
		contact.save()

		succ ='Your message has been sent successfully'
		context = {'succ':succ, 'cartItems':cartItems}
		return render(request, 'pages/contact.html', context)

	context = {'cartItems':cartItems}
	return render(request, 'pages/contact.html', context)

def about(request):
	return render(request, 'pages/about.html', cartItems(request))

def privacyPolicy(request):
	return render(request, 'quickLink/privacyPolicy.html', cartItems(request))

def refundPolicy(request):
	return render(request, 'quickLink/refundPolicy.html', cartItems(request))

def termsService(request):
	return render(request, 'quickLink/termsService.html', cartItems(request))
