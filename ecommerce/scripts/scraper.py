from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.request
import random
from django.core.files import File

from store.models import *
from utilisateurs.models import Account

baseUrl='https://us.shein.com/style'

# ---- PRODUCT LIST URL ---
url = 'https://us.shein.com/category/Kids-FW2020-sc-00827906.html?ici=us_tab04navbar02&srctype=category&userpath=category%3EKIDS%3EFW%202020&scici=navbar_KidsHomePage~~tab04navbar02~~2~~webLink~~SPcCccKidsCategory~~0~~50000'

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}

# -------------- extract all product links from a product list ------------------
r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')
productList = soup.find_all('div', class_='c-goodsitem__ratiowrap')
productLinks = []

for item in productList:
    for link in item.find_all('a', href=True):
        productLinks.append(baseUrl + link['href'])

# ------ SCRAP AND ISERT PRODUCT IN DATABASE ------
cat = Category.objects.get(id=3)
user = Account.objects.get(email='aziza@gmail.com')

driver = webdriver.Chrome()
j=1
for productLink in productLinks:
    driver.get(productLink)
    soup = BeautifulSoup(driver.page_source,"lxml")

    if soup.find('div', class_='product-intro__head-name') is None:
        continue
    else:
        title=soup.find('div', class_='product-intro__head-name').text.strip()

        descrip=''
        for i in soup.find_all('div', class_='product-intro__description-table-item'):
            key = i.find('div', class_='key').text.strip()
            val = i.find('div', class_='val').text.strip()
            keyVal = key+' '+val
            descrip = descrip+" | "+keyVal

        price = random.randrange(10,20)
        quantity = random.randrange(100,200)

        if soup.find('img', class_='j-verlok-lazy loaded') is None:
            continue
        else:
            imglink = 'http:' + soup.find('img', class_='j-verlok-lazy loaded').get('src')
            imglink = imglink.replace('220x293','635x550')  # IMAGE SIZE
            urllib.request.urlretrieve(imglink,'zzb_'+str(j)+'.jpg')

            product = Product(title=title, description=descrip, price=price, quantity=quantity, creator=user, category=cat)
            product.save()

        # imgLink=soup.find('img', class_='j-verlok-lazy loaded')
        # print(imgLink.get('src'))
        # urllib.request.urlretrieve('http:'+imgLink.get('src'),title+'.jpg')

        # users = Account.objects.all()
        # pr = Product.objects.get(title=title)
        # for us in users:
        #     r = random.randrange(1,5)
        #     Review(product=pr, customer=us, rating=r)

    print('product ('+str(j)+') : added')
    j=j+1
    print('-------------------------------')
driver.quit()