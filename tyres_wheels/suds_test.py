# -*- coding: utf-8 -*-
from suds.client import Client, WebFault
from suds.transport.http import HttpTransport

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys


# Отладочная информация
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)
# logging.getLogger('suds.xsd.schema').setLevel(logging.DEBUG)
# logging.getLogger('suds.wsdl').setLevel(logging.DEBUG)

# Дополнительный класс для корректной обработки HTTP-заголовков ответа SOAP-запроса
class MyTransport(HttpTransport):
    def __init__(self, *args, **kwargs):
        HttpTransport.__init__(self, *args, **kwargs)
        self.last_headers = None

    def send(self, request):
        result = HttpTransport.send(self, request)
        self.last_headers = result.headers
        return result

username = 'sa01614'
password = 'a8Q1Ts5Ya2'

# --- Входные данные ---
# Адрес WSDL-описания сервиса Campaigns (регистрозависимый)
CampaignsURL = 'http://api-b2b.4tochki.ru/WCF/ClientService.svc?wsd'

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = 'ТОКЕН'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = 'ЛОГИН_КЛИЕНТА'

# --- Подготовка, выполнение и обработка запроса ---
# Создание HTTP-заголовков запроса
headers = {
    #"Authorization": "Bearer " + token,         # OAuth-token. Использование слова Bearer обязательно
    "login": username,
    "password": password                # Логин клиента рекламного агентства
    #"Accept-Language": "ru",                    # Язык ответных сообщений
}

# Конструктор SOAP-клиента
client = Client(CampaignsURL)
client.set_options(transport=MyTransport())     # Установка дополнительно класса для отправки запросов
client.set_options(headers=headers)             # Установка HTTP-заголовков запроса


# Создание тела запроса
params = {
    "filter": {                   # Критерий отбора кампаний. Для получения всех кампаний должен быть пустым
    "code_list": ['2622800']                # Имена параметров, которые требуется получить
    }
}

# Выполнение запроса
# try:
result = client.service.GetGoodsPriceRestByCode(**params)
print("RequestId: {}".format(client.options.transport.last_headers.get("requestid",False)))
print("Информация о баллах: {}".format(client.options.transport.last_headers.get("units", False)))
