import datetime

from bs4 import BeautifulSoup
import requests
from time import sleep
import lxml

#
# from config import TOKEN, BOT_URL, CHAT_ID
from send_result import proxy_list
from cred import TOKEN, CHAT_ID

BOT_NAME = 'GovParseBot'
BOT_URL = 'https://api.telegram.org/bot'

# TEXT = ''

jar = requests.cookies.RequestsCookieJar()
general_url = 'https://zakupki.gov.ru' #'http://95.167.245.92'#
url_parse = "/epz/dizk/search/results.html"
url = general_url + url_parse
# proxy_list = []

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "content-type": "text/plain",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/plain, */*",
    "Referer": "https://zakupki.gov.ru/epz/dizk/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&published=on&ur=on"
}


# Get data from target page
def get_data():
    resp = requests.get(url, headers=headers, cookies=jar)
    soup = BeautifulSoup(resp.text, 'lxml')
    urls_t = soup.findAll('div', class_="registry-entry__form")

    ids = []
    for string in urls_t:
        link = general_url + string.find('a').get('href')
        dizkid_entry = link.rfind('=')
        dizkid = link[dizkid_entry + 1:]
        ids.append(dizkid)

    return ids  # list
    # sleep(101)


# try write data
# we want to have a list for 100 times
def write_data():

    # if len(proxy_list) > 100: # we want to have a list for 100 times
    #     del proxy_list[:10]

    f = open('send_result.py', 'w')
    f.write('proxy_list = ' + str(proxy_list))
    f.close()

    f = open('log.txt', 'a')
    f.write(str(datetime.datetime.now()) +  ' ids_proxy = ' + str(proxy_list) + '\n')
    f.close()

    print(datetime.datetime.now(), 'proxy_list from write_data  -', proxy_list)
    return proxy_list


# try to confirm new data and previous data
def confirm_data():

    target_list = []
    for i in get_data():
        if i not in proxy_list:
            target_list.append(i)
    proxy_list.extend(target_list)
    #proxy = list(set(proxy_list))
    if len(proxy_list) > 100: # we want to have a list for 100 times
        del proxy_list[:10]
    #proxy_list = proxy
    if target_list is not False:
        print(datetime.datetime.now(), 'target_list from confirm_data =', target_list)
    return target_list


# try to send diff data
def send_url():

    target_list_links = []

    for ii in confirm_data():
        target_link = 'https://zakupki.gov.ru/epz/dizk/dizkCard/generalInformation.html?dizkId=' + ii
        target_list_links.append(target_link)
        #print(target_link)

    for s in target_list_links:
        if target_list_links[0] is not None:
            TEXT = s
            respp = requests.get(url=BOT_URL + TOKEN + '/sendMessage?' + 'chat_id=' + CHAT_ID + '&' + 'text=' + TEXT)

            print(respp)
            sleep(3)


    #print('proxy_list from send_url -', proxy_list)
    if target_list_links is True:
        print('target_list_links from send_url -', target_list_links)
    #return target_list_links
    write_data()
    confirm_data()
    # sleep(101)

print('proxy_list -', proxy_list)

