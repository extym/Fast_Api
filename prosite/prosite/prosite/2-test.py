import logging
from suds.client import Client
from suds.wsse import *
from datetime import timedelta,date,datetime,tzinfo
import requests
from requests.auth import HTTPBasicAuth
import suds_requests
name = 'noreply@brain-trust.ru'
passwd = 'tojo2Xe'

# username=input('Username:')
# password=input('password:')
session = requests.session()
session.auth=(name, passwd)
point = 2011681
WSDL_URL = f'https://1cfresh.com/a/sbm_demo/{str(point)}/ws/SiteExchange?wsdl'


client = Client(WSDL_URL, faults=False, cachingpolicy=1, location=WSDL_URL, transport=suds_requests.RequestsTransport(session))


def addSecurityHeader(client,username,password):
    security=Security()
    userNameToken=UsernameToken(username,password)
    timeStampToken=Timestamp(validity=600)
    security.tokens.append(userNameToken)
    security.tokens.append(timeStampToken)
    client.set_options(wsse=security)

addSecurityHeader(client,name,passwd)

result = client.service.__getitem__
print(result)

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)