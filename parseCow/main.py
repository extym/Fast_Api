from bs4 import BeautifulSoup
import requests
from time import sleep
import lxml
#
# from config import TOKEN, BOT_URL, CHAT_ID
# from send_result import ids_proxy

TOKEN = "5491812290:AAFZbUoG0hjH9N8PUb9WCQ0ayvDOWLex4jw" # - t.me/GovParseBot #"5214618946:AAGIS6raKgn28A4-J_1s_9yTp5noZoGtrjw"
BOT_NAME = 'GovParseBot'
BOT_URL = 'https://api.telegram.org/bot'
CHAT_ID = '471124111'
#TEXT = ''

jar = requests.cookies.RequestsCookieJar()
general_url = 'https://zakupki.gov.ru'
url_parse = "/epz/dizk/search/results.html"
url = general_url + url_parse

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "content-type": "text/plain",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/plain, */*",
    "Referer": "https://zakupki.gov.ru/epz/dizk/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&published=on&ur=on"
}


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


def check_data():
    #from send_res import ids_proxy
    target_list = []
    for i in get_data():
        if i not in save_data(): #ids_proxy:
            target_list.append(i)

    f = open('send_result.py', 'w')
    f.write('ids_proxy = ' + str(get_data()))
    f.close()

    return target_list


print(get_data())


def send_url():
    # global target_list_links
    target_list_links = []

    for ii in check_data():
        target_link = 'https://zakupki.gov.ru/epz/dizk/dizkCard/generalInformation.html?dizkId=' + ii
        target_list_links.append(target_link)
        print(target_link)

    for s in target_list_links:
        if target_list_links[0] is not None:
            TEXT = s
            respp = requests.get(url=BOT_URL + TOKEN + '/sendMessage?' + 'chat_id=' + CHAT_ID + '&' + 'text=' + TEXT)
            # resp = requests.post(url=url_send, headers=headers, data=json.dumps(s))
            print(respp)
            sleep(3)

    return target_list_links
    #sleep(101)

def save_data():
    f = open('send_res.py', 'w')
    f.write('ids_proxy = ' + str(get_data()))
    f.close()
    ids_proxy = get_data()
    return ids_proxy

#print(send_url())