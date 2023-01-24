import ast
import logging
from lxml import etree
from zeep import Client, helpers, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
import datetime
from zeep import xsd

username = 'izotov.a'
password = 'k2W6C4pd'
# username = 'noreply@brain-trust.ru'
# password = 'tojo2Xe'
history = HistoryPlugin()

# username=input('Username:')
# password=input('password:')

point = 2011681
WSDL_URL =  'http://api.owl1975.ru/ut11/ws/Exchange_3_0_1_1?wsdl#Exchange_3_0_1_1' #f'https://1cfresh.com/a/sbm_demo/{str(point)}/ws/SiteExchange?wsdl'
# WSDL_URL = 'https://1cfresh.com/a/sbm/2022888/ws/SiteExchange?wsdl'
#
time_now = datetime.datetime.now()
print(time_now)

#try:
wsdl = WSDL_URL
session = Session()
session.auth = HTTPBasicAuth(username, password)
#client = Client('http://api.owl1975.ru/ut11', plugins=[history])
settings = Settings(strict=False, xml_huge_tree=True, raw_response=True)
client = Client(WSDL_URL, transport=Transport(session=session), plugins=[history]) #, settings=settings)
#
# session.proxies = {"https": f"socks5://{settings.STATIC_PROXY}"}
# transport = Transport(session=session, timeout=(5, 30))
#client = Client(wsdl, transport)
# request = client.service.GetAmountAndPrices(time_now)

#with client.settings(raw_response=True):
  #response = client.service.myoperation()
response = client.service.Download #GetAmountAndPrices(time_now)
  # response is now a regular requests.Response object
  # assert response.status_code == 200
  # assert response.content
print(response)
#print(etree.tostring(history.last_sent["envelope"], encoding="unicode", pretty_print=True))
#print(history.last_sent)
#print(history.last_received)


print(response.status)

data = helpers.serialize_object(response)
print(type(data), data)


client.transport.session.close()