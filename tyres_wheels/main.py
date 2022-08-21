import requests
from flask import Flask, request, app
import json
address = 'https://b2b.kolrad.ru/json/hannover/'
num = 0
page = 'page' + str(num)
contract = '/contract68/?'
Token = '$1$5lOhoSsQ$eOxkDECAapvsE6qAkFE8h1'
vendor = 0

link = address + page + contract + 'token=' + Token + '&vendor=' + str(vendor)
# get start page & pages
resp = requests.get(link)
txt = requests.get(link).text
pages = txt[88:92]
# err_before = txt[850:944]
err_after = txt[583:1078]#[983:1078]
# number = resp.json(["pages"])
# print(number)

print(pages)

print('!!! - ' + err_after)
# with open("developer.json", "a") as write_file:
#     json.dump(resp, write_file) # encode dict into JSON
# print("Done writing JSON data into .json file")

from requests.exceptions import HTTPError

try:
    # response = requests.get('https://httpbin.org/get')
    resp.raise_for_status()
    # access JSOn content
    jsonResponse = resp.json()
    print("Entire JSON response")
    print(jsonResponse)

except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')


r = resp.encoding
pagess = resp.raise_for_status()
# pagess = resp.json()
print(pagess)

print("111 - " + r)