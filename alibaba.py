import requests
from bs4 import BeautifulSoup
import csv

tur_url = 'https://www.alibaba.com/products/laptops.html?ta=y'
#a quick web scraping of alibaba
def bundle_links(self):
    req = requests.get(self)
    a=[]
    if req.ok:
        soup = BeautifulSoup(req.text,'lxml')
        links = soup.find_all('a',class_='elements-title-normal one-line')
        for link in links:
            link=link.get('href').replace('//','https://')
            a.append(link)
    return a


def get_link(url):
    req = requests.get(url)
    if req.ok:
        soup = BeautifulSoup(req.text,'lxml')
        print(f'{req.status_code}')
        return soup
    else:
        print('geofrrry')


def convert(cash):
    request1 = requests.get('https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=ZMW')

    soup = BeautifulSoup(request1.text, 'lxml')
    c_curr = soup.find('p', class_='result__BigRate-sc-1bsijpp-1 iGrAod')
    v = float(c_curr.text.split(' ')[0])
    w=float(round( float(cash) * round(v, 3)))
    print (w)
    return w

def get_deets(soup):
    data = {}
    price_list = []
    TITLES = soup.find_all('h1',class_ = 'module-pdp-title')
    try:
     PRICES = soup.find_all('span',class_ = 'pre-inquiry-price')
    except:
     PRICES =soup.find_all('span',class_='ma-ref-price')
     print(PRICES)
     pass
    for title in TITLES:
        try:
          data['title'] = title.get('title')
        except:
            pass
        n = 0
        for price in PRICES:
            while n<=1:
             p=float(price.text.split('$')[1])
             price_list.append(convert(p))
             n+=1


    data['price'] = price_list
    return data

def write_csv(data,url):
    with open('output.csv','a') as f:
        writer = csv.writer(f)
        daat = [data['title'],data['price'],url]
        writer.writerow(daat)






def main():
  
   z=bundle_links(tur_url)
   print(z)
   for link in z:
    w = get_deets(get_link(link))
    write_csv(w, link)





if __name__ == '__main__':
    main()
