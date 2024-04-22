from bs4 import BeautifulSoup
import requests
from time import sleep
import lxml


# finland_url_reg = 'https://finlandvisa.fi/register'


jar = requests.cookies.RequestsCookieJar()

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "content-type": "text/plain",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/plain, */*"
}



def get_page(url):
    answer = requests.get(url, headers, cookies=jar)
    print(111, answer.cookies.items())
    print(222, answer.text)
