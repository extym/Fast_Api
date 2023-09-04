from bs4 import BeautifulSoup
import requests
from time import sleep
import lxml


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "content-type": "text/plain",
    "accept-encoding": "gzip, deflate, br",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
url = 'https://neooilmarket.ru/catalog?page=2'

def get_data():
    proxy = []
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    oil_name = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('span', class_ = 'hidden').text
    link_for_the_oil = soup.find('div', class_="c-goods__left").find('a', class_="c-goods__img").get('href')
    print(link_for_the_oil)  #https://neooilmarket.ru/maslo-dlya-mototehniki/neo-expert-marine-outboard-2t-api-tcs-4

    big_image = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('img', class_ = 'mg-product-image js-catalog-item-image').get('src')
    vendor_code = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('input', class_="js-onchange-price-recalc").get("data-code")
    data_id = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('input', class_="js-onchange-price-recalc").get("data-id")
    value = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('span', class_="c-variant__name variantTitle").text.strip()
    price = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")\
        .find('div', class_="c-goods__price--current product-price js-change-product-price").find('span').text
    urls_t = soup.find('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")

    catalog = soup.findAll('div', class_="l-col min-0--12 min-375--6 min-768--4 min-990--3 min-1025--4 c-goods__trigger")

    print(len(catalog))
    print(urls_t)
    proxy.append((oil_name, big_image, vendor_code, data_id, value, price))
    return proxy



get_data()