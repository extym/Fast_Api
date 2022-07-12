from bs4 import BeautifulSoup
import lxml
import requests
from time import sleep
import time
import schedule
import datetime
import json
import telebot
from config import TOKEN, BOT_URL, CHAT_ID
from send_result import ids_proxy

TEXT = ''
bot = telebot.TeleBot(TOKEN)
jar = requests.cookies.RequestsCookieJar()
general_url = 'https://zakupki.gov.ru'
url_parse = "/epz/dizk/search/results.html"
url = general_url + url_parse
# https://api.telegram.org/bot5214618946:AAGIS6raKgn28A4-J_1s_9yTp5noZoGtrjw/sendMessage?chat_id={}&text={}
url_send = BOT_URL + TOKEN + '/sendMessage?' + 'chat_id=' + CHAT_ID + '&' + 'text=' + TEXT
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36", #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "content-type": "text/plain",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/plain, */*",
    "Referer": "https://zakupki.gov.ru/epz/dizk/search/results.html?morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D0%BE%D0%B1%D0%BD%D0%BE%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&published=on&ur=on"
}

header = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36", #"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
    "accept-encoding": "gzip, deflate, br",
    "accept": "application/json, text/plain, */*",
}


def get_data():
    resp = requests.get(url, headers=headers, cookies=jar) #, timeout=120)
    soup = BeautifulSoup(resp.text, 'lxml')
    so = soup.find('div', class_="registry-entry__form")
    urls_t = soup.findAll('div', class_="registry-entry__form")

    # global ids_proxy
    # global links
    # global ids
    # ids_proxy = []

    ids = []
    links = []
    for link in urls_t:
        link2 = general_url + link.find('a').get('href')
        links.append(link2)

        dizkId_entry = link2.rfind('=')
        dizkId = link2[dizkId_entry + 1:]

        ids.append(dizkId)


# def result():
    target_list = []
    for i in ids:
        if i not in ids_proxy:
            target_list.append(i)
            # f = open('send_result.py', 'a')
            # f.write(str(datetime.datetime.now()) + 'ids_proxy = '+ str(target_list))
            # f.close()
    f = open('send_result.py', 'w')
    f.write('ids_proxy = ' + str(ids))
    f.close()

    print(target_list)
    # global target_list_links
    target_list_links = []

    for ii in target_list:
        target_link = 'https://zakupki.gov.ru/epz/dizk/dizkCard/generalInformation.html?dizkId=' + ii
        target_list_links.append(target_link)
        print(target_link)

    for s in target_list_links:
        if target_list_links[0] is not None:

            TEXT = s
            respp = requests.get(url=BOT_URL + TOKEN + '/sendMessage?' + 'chat_id=' + CHAT_ID + '&' + 'text=' + TEXT)
            #resp = requests.post(url=url_send, headers=headers, data=json.dumps(s))
            print(respp)
            sleep(2)
        else:
            pass


    return target_list_links

#print(get_data())

@bot.message_handler(commands=['start'])
def handle_start(message):

    bot.send_message(message.from_user.id, 'Добро пожаловать!') #, reply_markup=user_markup)
    for link in get_data():
        bot.send_message(message.chat.id, link + '\n')
        sleep(1)



# schedule.every(2).minutes.do(get_data)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

#c = r_get.request.headers #what is headers we send
#print(resp.text)
#print(link)



bot.polling(none_stop=True)



# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
