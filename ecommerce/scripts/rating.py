from store.models import Account, Product, Review
import random

comment = {
    1 : 'Very Bad Product',
    2 : 'Poor ☹',
    3 : 'OK !',
    4 : 'Good Product',
    5 : 'Excelent Product I love it ❤'
}

productList = list(Product.objects.all())
products = productList[300:302]

emailList =('asma@gmail.com',)
for email in emailList:
    customer = Account.objects.get(email=email)
    for product in products:
        i = random.randrange(1,6)
        review = Review(product=product, customer=customer, rating=i, comment=comment[i])
        review.save()
        print(customer.email+' ==> '+str(i)+' : '+comment[i])

