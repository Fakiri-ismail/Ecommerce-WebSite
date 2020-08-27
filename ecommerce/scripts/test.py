from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import urllib.request


url = 'https://us.shein.com/Men-Lace-up-Decor-Colorblock-Chunky-Sneakers-p-1400290-cat-2093.html?scici=navbar_MenHomePage~~tab03navbar06banner02~~6_2~~real_2093~~SPcCccMenCategory~~0~~50000'

driver = webdriver.Chrome()
driver.get(url)
soup = BeautifulSoup(driver.page_source,"lxml")
imglink = soup.find('img', class_='j-verlok-lazy loaded').get('src')
print(imglink)
imglink = imglink.replace('220x293','635x550')
print(imglink)
driver.quit()