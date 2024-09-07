import requests
import json
import time
import shutil
import zipfile
from requests.auth import HTTPBasicAuth


def confirm_data_transfer(app_url, user):
    url = app_url + "/hs/dt/storage/integration/get"
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))
    headers = {"IBSession": "start"}
    response = requests.post(url, auth=credentials, headers=headers, allow_redirects=False)
    put_location = response.headers.get('Location')
    put_cookie = response.headers.get('Set-Cookie')

    headers = {"Cookie": put_cookie, "IBSession": "finish"}
    response = json.loads(requests.put(put_location,
                                       auth=credentials,
                                       headers=headers,
                                       allow_redirects=False).text)

    # print(2222, response)
    if response.get('general').get('response') == 10404:
        print('Данные для подтверждения отсутствуют')
        return False

    job_id = response.get('result').get('id')

    headers = {"IBSession": "start"}
    url = app_url + "/hs/dt/storage/jobs/" + job_id

    response = requests.get(url, auth=credentials, headers=headers, allow_redirects=False)

    get_location = response.headers.get('Location')
    get_cookie = response.headers.get('Set-Cookie')

    headers = {"Cookie": get_cookie}
    job_done = False

    while not job_done:
        response = requests.get(get_location, auth=credentials, headers=headers, allow_redirects=False)
        status_code = json.loads(response.text).get('general').get('response')
        time.sleep(2)
        print(4444, status_code)

        if status_code != 10202:
            job_done = True
    print(4455, response.text)
    job_status_code = json.loads(response.text).get('general').get('response')
    if job_status_code != 10200:
        print(json.loads(response.text).get('general').get('message'))
        return False
    else:
        file_id = json.loads(response.text).get('result').get('id')
        file_url = app_url + "/hs/dt/storage/files/" + file_id
        headers = {"IBSession": "start"}
        print(file_url)
        response = requests.get(file_url, headers=headers, auth=credentials, allow_redirects=False)

        print(response.text)

        get_location = response.headers.get('Location')
        get_cookie = response.headers.get('Set-Cookie')
        headers = {"Cookie": get_cookie}

        response = requests.get(get_location, stream=True, auth=credentials, headers=headers, allow_redirects=False)
        with open('result.zip', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        f = 'result.zip'
        z = zipfile.ZipFile(f, "r")
        zinfo = z.namelist()
        for name in zinfo:
            if name == "manifest.json":
                with z.open(name) as f1:
                    manifest = json.loads(f1.read().decode('utf-8'))

        result = []
        result_map = {"file": manifest.get('upload')[0].get('file'),
                      "version": manifest.get('upload')[0].get('version'),
                      "handler": manifest.get('upload')[0].get('handler'),
                      "response": 10200,
                      "error": False,
                      "message": ""}
        result.append(result_map)
        payload = json.dumps({"result": result})
        headers = {"IBSession": "start"}
        url = app_url + "/hs/dt/storage/integration/confirm"

        response = requests.post(url, auth=credentials, headers=headers, allow_redirects=False)
        put_location = response.headers.get('Location')
        put_cookie = response.headers.get('Set-Cookie')

        headers = {"Cookie": put_cookie, "IBSession": "finish"}

        response = json.loads(requests.put(put_location,
                                           auth=credentials,
                                           data=payload,
                                           headers=headers,
                                           allow_redirects=False).text)
        print(response)


server = "https://1cfresh.com"
reg = "a/adm/hs/ext_api/execute"
tenant_id = 1
app_name = "ea"
# Имя пользователя и пароль служебного пользователя, под которым выполняется интеграция.
username = "new_name"
password = "123Qwer"
user = {"login": username, "password": password}

app_url = "{server}/a/{app_name}/{tenant_id}".format(server=server, app_name=app_name, tenant_id=tenant_id)

# 6. Получить данные из 1С
# Необходимо запросить данные из 1С.
# Результат: Временный файл в котором содержится ED с реквизитами счета
# В 1С в регистре e1cib/list/РегистрСведений.ДокументыИнтеграцииCRM не должно быть записей с типом:
# Состояние = Подготовлено к отправке
# Описания сервиса получения данных - https://its.1c.ru/db/fresh#content:19956672:hdoc
confirm_data_transfer(app_url, user)