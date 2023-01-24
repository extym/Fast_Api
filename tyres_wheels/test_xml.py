


filter = ['2622800']
# filter = {'filter':{'code_list': ['2622800']}}

login = 'sa01614'
password = 'a8Q1Ts5Ya2'

wsdl = 'http://api-b2b.4tochki.ru/WCF/ClientService.svc?wsdl'
login = 'sa01614'
password = 'a8Q1Ts5Ya2'
#
#
# client = Client(wsdl, username=login, password=password)
# result = client.service.GetGoodsPriceRestByCode(filter)



from suds.client import Client, WebFault
from suds.transport.http import HttpTransport

# Метод для корректной обработки строк в кодировке UTF-8 как в Python 3, так и в Python 2
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x


# Отладочная информация
import logging

logging.basicConfig(level=logging.DEBUG)
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


# --- Входные данные ---
# Адрес WSDL-описания сервиса Campaigns (регистрозависимый)
# CampaignsURL = 'https://api.direct.yandex.com/v5/campaigns?wsdl'

# OAuth-токен пользователя, от имени которого будут выполняться запросы
token = 'ТОКЕН'

# Логин клиента рекламного агентства
# Обязательный параметр, если запросы выполняются от имени рекламного агентства
clientLogin = 'ЛОГИН_КЛИЕНТА'

# --- Подготовка, выполнение и обработка запроса ---
# Создание HTTP-заголовков запроса
headers = {
    #"Authorization": "Bearer " + token,         # OAuth-token. Использование слова Bearer обязательно
    "login": login,                # Логин клиента рекламного агентства
    "password": password
    #"Accept-Language": "ru",                    # Язык ответных сообщений
}

# Конструктор SOAP-клиента
client = Client(wsdl, location='http://api-b2b.4tochki.ru/WCF/ClientService.svc')
client.set_options(transport=MyTransport())     # Установка дополнительно класса для отправки запросов
#client.set_options(headers=headers)             # Установка HTTP-заголовков запроса


# Создание тела запроса

params = {
    # "login": login,
    # "password": password,
    "filter": {
    "code_list": ["2622800", ""],
    "wrh_list": [1, 2],
    "include_paid_delivery": False
    }
}

# Выполнение запроса
#try:
result = client.service.GetGoodsPriceRestByCode(**params)
# print ("RequestId: {}".format(client.options.transport.last_headers.get("requestid",False)))
# print ("Информация о баллах: {}".format(client.options.transport.last_headers.get("units", False)))
# for campaign in result:
#     print ("Рекламная кампания: {} №{}".format(u(campaign['Name']), campaign['Id']))
# #
# except WebFault as err:
#     print ("Произошла ошибка при обращении к серверу API Директа.")
#     print ("Код ошибки: {}".format(err.fault['detail']['FaultResponse']['errorCode']))
#     print ("Описание ошибки: {}".format(u(err.fault['detail']['FaultResponse']['errorDetail'])))
#     print ("RequestId: {}".format(err.fault['detail']['FaultResponse']['requestId']))
#
# except:
#     err = sys.exc_info()
#     print ('Произошла ошибка при обращении к серверу API Директа: ' + str(err[1]))
print('from_rest_xml', result)