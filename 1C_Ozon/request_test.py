import requests

def send_smth_post(data):
    url = ''
    heads = ''
    resp = requests.post(url, headers=heads, json=data)

    print(resp.text)