import requests
from lxml import etree


import ast
import logging
from zeep import Client, helpers, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import datetime


username = 'sa01614'
password = 'a8Q1Ts5Ya2'

# username = 'izotov.a'
# password = 'k2W6C4pd'
# username = 'noreply@brain-trust.ru'
# password = 'tojo2Xe'
history = HistoryPlugin()

# username=input('Username:')
# password=input('password:')

point = 2011681
WSDL_URL =  'http://api-b2b.4tochki.ru/WCF/ClientService.svc?wsdl'
#WSDL_URL =  'http://api.owl1975.ru/ut11' #f'https://1cfresh.com/a/sbm_demo/{str(point)}/ws/SiteExchange?wsdl'
# WSDL_URL = 'https://1cfresh.com/a/sbm/2022888/ws/SiteExchange?wsdl'
#
time_now = datetime.datetime.now()
print(time_now)

#try:
wsdl = WSDL_URL
session = Session()
session.auth = HTTPBasicAuth(username, password)
#client = Client('http://api.owl1975.ru/ut11', plugins=[history])
# settings = Settings(strict=False, xml_huge_tree=True, raw_response=True)
settings = Settings(extra_http_headers={'login':username, 'password':password})

client = Client(WSDL_URL, transport=Transport(session=session), plugins=[history], settings=settings)
# request = client.service.GetAmountAndPrices(time_now)

filter = {
    "login": username,
    "password": password,
    'filter':{'code_list': ['2622800']},
} #{'code_list':['2622800', '2622800']}
#with client.settings(raw_response=True):
  #response = client.service.myoperation()
response = client.service.GetGoodsPriceRestByCode(**filter)
  # response is now a regular requests.Response object
  # assert response.status_code == 200
  # assert response.content
print(response)


# for hist in [history.last_sent, history.last_received]:
#     print(etree.tostring(hist["envelope"], encoding="unicode", pretty_print=True))
print(etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True))
#print (etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True))

# print (history.last_sent)
# print (history.last_received)


data = helpers.serialize_object(response, dict)
print(type(data), data)


# logging.basicConfig(level=logging.INFO)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)
# logging.getLogger('suds.transport').setLevel(logging.DEBUG)

client.transport.session.close()