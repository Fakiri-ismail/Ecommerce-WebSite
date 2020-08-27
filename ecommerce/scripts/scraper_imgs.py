from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.request

url = 'https://us.shein.com/Men-Sneakers-c-2093.html?icn=men-sneakers&ici=us_tab03navbar06banner02&adp=1400290&srctype=category&userpath=category%3EMEN%3ESHOES-ACCESSORIES%3EMen-Sneakers&scici=navbar_MenHomePage~~tab03navbar06banner02~~6_2~~real_2093~~SPcCccMenCategory~~0~~50000'

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
imgLinks = []

# -------- GET LINK OF ALL IMAGES ----------------
for item in productList:
    for link in item.find_all('a'):
        for img in link.find_all('img', class_='j-verlok-lazy'):
            imgLinks.append('http:'+img['data-src'])

# -------------- IMAGES DOWNLOAD ------------------
i=1
for imgLink in imgLinks:
    urllib.request.urlretrieve(imgLink,str(i)+'.jpg')
    i=i+1
