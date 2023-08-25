import requests
from bs4 import BeautifulSoup



def gomaji(url):
  res = requests.get(url)
  soup = BeautifulSoup(res.text,"lxml")

  all = soup.find_all('div','product-card mm-product-card border bg-white')


  ls=[]

  for i in all:
    product = i.find('h3','ellipsis').text.strip()
    describe = i.find('h4','ellipsis t-darkgray').text.strip()
    sub_price = i.find('div','current t-orange').text.strip()
    price= sub_price.replace('\n起','').replace('$','')
    sub_link= i.find('a')
    link='https://www.gomaji.com'+sub_link['href']
    info=(product,describe,price,link)
    ls.append(info)

  return ls

ls1=[]

for i in range(18):
  if i == 7:
    continue
  else:
    url=f'https://www.gomaji.com/ch/700097?city={i}&dist_group=0'
    ls1.extend(gomaji(url))

print(ls1)

import pandas as pd

df=pd.DataFrame(ls1,columns=['產品名稱','描述','價錢','連結'])
df.to_csv('coupon1.csv')