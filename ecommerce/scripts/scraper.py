import requests
import urllib.request
from bs4 import BeautifulSoup
from django.core.files import File

baseUrl='https://us.shein.com/style'
url = 'https://us.shein.com/style/Vacation-Dresses-sc-00100461.html?icn=style&ici=ma_tab01navbar05menu01dir01&srctype=category&userpath=category%3EFEMME%3EROBES%3ESHOPPEZ%20PAR%20STYLE%3EBoh%C3%A8me&scici=navbar_WomenHomePage~~tab01navbar05menu01dir01~~5_1_1~~itemPicking_00100461~~SPcCccWomenCategory~~0~~50001&is_manual_change_site=0&ref=ma&ret=us&from_country=ma'
headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'http://www.wikipedia.org/',
    'Connection': 'keep-alive',
}

r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')
productList = soup.find_all('div', class_='c-goodsitem__ratiowrap')
productLinks = []

for item in productList:
    for link in item.find_all('a', href=True):
        productLinks.append(baseUrl + link['href'])

testlink='https://us.shein.com/style/Floral-Print-Cami-Dress-p-1201607-cat-1727.html?scici=navbar_WomenHomePage~~tab01navbar05menu01dir01~~5_1_1~~itemPicking_00100461~~SPcCccWomenCategory~~0~~50001'
r = requests.get(testlink, headers=headers)
soup = BeautifulSoup(r.content, 'lxml')
print(type(soup))
print(soup.find_all('div', class_='swiper-slide product-intro__main-item cursor-zoom-in'))