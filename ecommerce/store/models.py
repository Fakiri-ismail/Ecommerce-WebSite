from django.db import models
from utilisateurs.models import Account

class Category(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Product(models.Model):
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=3000)
	price = models.FloatField()
	quantity = models.IntegerField(default=0, null=True)
	is_hide = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)

	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
	creator = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)

	def __str__(self):
		return self.title

	@property
	def get_images(self):
		return self.productimage_set.all()
	
	@property
	def get_image(self):
		return self.productimage_set.all()[0]

class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
	image = models.ImageField(upload_to='products', null=True, blank=True)

	def __str__(self):
		return self.product.title

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	customer = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return 'transaction ' + str(self.id) + str(self.date_ordered)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.order.transaction_id

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
	address = models.CharField(max_length=200, null=False)
	tel = models.CharField(max_length=10, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address

class Contact(models.Model):
	email = models.EmailField(max_length=60)
	message = models.CharField(max_length=6000, null=False)

	def __str__(self):
		return self.email

class Review(models.Model):
	customer = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
	rating = models.IntegerField()

	def __str__(self):
		return self.customer.email + ' ==> ' + self.product.title + ' : ' + str(self.rating)
