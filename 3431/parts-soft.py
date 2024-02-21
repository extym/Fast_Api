from requests.auth import HTTPBasicAuth
from cred import admin_ps_login, admin_ps_pass, ps_link
from base64 import b64encode
import requests
from requests import Session




def basic_auth():
    token = b64encode(f"{admin_ps_login}:{admin_ps_pass}".encode('utf-8')).decode("ascii")
    return token


def get_client():
    session = Session()
    session.auth = (admin_ps_login, admin_ps_pass)

    return session.auth


def get_smth(metod):
    url = ps_link + metod
    # session = Session()
    # session.auth = (admin_ps_login, admin_ps_pass)
    # answer = session.get(url)
    token_ps = HTTPBasicAuth(admin_ps_login, admin_ps_pass)
    answer = requests.get(url, auth=token_ps)

    print(answer.text)

get_smth('/regions.json')