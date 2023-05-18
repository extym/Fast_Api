import requests


def post_smth(data, url, magic_link):
    headers = {
        "Autorisation": magic_link
    }
    url = 'http://localhost:7770/json'
    result = requests.post(url, headers=headers, json=data)

    # print(result.text)