import requests
import json
import urllib3
import time
import sys
from requests.auth import HTTPBasicAuth


# 1. Создание пользователя


def user_for_crm_integration(server, reg, credentials, tenant_id, postfix):
    # Для создания пользователя используется API менеджера сервиса
    #  https://its.1c.ru/db/freshsm

    url = server + reg
    account_id = get_account_id(url, credentials)
    if account_id is None:
        print("Не удалось получить account_id")
        return None

    if not has_tenant(url, credentials, account_id, tenant_id):
        print('Не найдена область {tenant_id}'.format(tenant_id=tenant_id))
        return None

    user = create_user(url, credentials, account_id, tenant_id, postfix)
    if user is None:
        print("Пользователь не создан.")
        return None

    return user


def get_account_id(url, credentials):
    urllib3.disable_warnings()
    headers = {}
    general = {"type": "ext", "method": "account/list"}
    body = json.dumps({"general": general})

    response = requests.post(
        url,
        auth=credentials,
        data=body,
        headers=headers,
        allow_redirects=False,
        verify=False)

    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию')
        return None

    response = json.loads(response.text)

    general = response['general']
    if general['response'] != 10200:
        print(general['message'])
        return None

    account_id = 0
    for account in response['account']:
        if account['role'] == 'owner':
            account_id = account['id']
            break

    if account_id == 0:
        print('Пользователь не является Владельцем абонента')
        return None

    return account_id


def get_tenant_list(url, credentials, account_id):
    urllib3.disable_warnings()
    headers = {}
    general = {"type": "ext", "method": "tenant/list"}
    auth = {"account": account_id}
    body = json.dumps({"general": general, "auth": auth})

    response = requests.post(
        url,
        auth=credentials,
        data=body,
        headers=headers,
        allow_redirects=False,
        verify=False)

    if response.status_code != 200:
        print(general['message'])
        return None

    response = json.loads(response.text)
    return response['tenant']


def has_tenant(url, credentials, account_id, tenant_id):
    tenant_list = (get_tenant_list(url, credentials, account_id))
    has_tenant = False
    for tenant in tenant_list:
        if tenant['id'] == tenant_id:
            has_tenant = True
            break

    return has_tenant


def create_user(url, credentials, account_id, tenant_id, postfix):
    urllib3.disable_warnings()

    headers = {}

    username = get_new_username(url, credentials, account_id, postfix)
    password = "123Qwer"

    general = {"type": "ext", "method": "account/users/create"}
    auth = {"account": account_id}
    body = json.dumps({"general": general,
                       "auth": auth,
                       "id": account_id,
                       "name": username,
                       "login": username,
                       "password": password,
                       "email_required": False,
                       "role": "user"})

    response = requests.post(
        url,
        auth=credentials,
        data=body,
        headers=headers,
        allow_redirects=False,
        verify=False)

    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию')
        return None

    response = json.loads(response.text)

    general = response['general']
    if general['response'] != 10200:
        print(general['message'])
        return None

    user = {"login": username, "password": password}

    add_user_to_tenant(url, credentials, account_id, tenant_id, user)

    return user


def get_new_username(url, credentials, account_id, postfix):
    return "new_name"


def add_user_to_tenant(url, credentials, account_id, tenant_id, user):
    urllib3.disable_warnings()
    headers = {}
    general = {"type": "ext", "method": "tenant/users/add"}
    auth = {"account": account_id}
    body = json.dumps({"general": general,
                       "auth": auth,
                       "id": tenant_id,
                       "login": user['login'],
                       "role": "api"})
    response = requests.post(
        url,
        auth=credentials,
        data=body,
        headers=headers,
        allow_redirects=False,
        verify=False)

    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию')
        return None

    response = json.loads(response.text)

    general = response['general']
    if general['response'] != 10200:
        print(general['message'])
        return None

    return


# 2. Включение интеграции


def setup_integration(app_url, user):
    credentials = (user.get('login'), user.get('password'))
    setup_name = "CRM to 1C for {user}".format(user=user['login'])
    settings_map = {"type": "crm",
                    "name": setup_name,
                    "use_notices": True,
                    "notice_settings": {
                        "url": "https://example.ru/cabinet/notice",
                        "authentication_type": "anonymous"}}

    url = app_url + "/hs/dt/storage/integration/setup/"
    headers = {"IBSession": "start"}

    response = requests.post(url, auth=credentials, headers=headers, allow_redirects=False)

    put_location = response.headers.get('Location')
    put_cookie = response.headers.get('Set-Cookie')

    headers = {"Cookie": put_cookie, "IBSession": "finish"}

    requests.put(put_location, auth=credentials, data=json.dumps(settings_map), headers=headers,
                 allow_redirects=False)


# 3. Проверка OData


def check_odata(app_url, user):
    if not check_odata_organization(app_url, user):
        return False

    if not check_odata_partners(app_url, user):
        return False

    if not check_odata_assortment(app_url, user):
        return False

    if not check_odata_pricelist(app_url, user):
        return False
    # Примеры запросов можно взять отсюда - https://its.1c.ru/db/fresh#content:19956692:hdoc
    return True


def check_odata_organization(app_url, user):
    print("Проверяем справочник Организации")
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))
    format_odata = "$format=json;odata=nometadata"
    company_keys = "Ref_Key,Description,ИНН,КПП,НаименованиеПолное,ОГРН,Префикс,ЮридическоеФизическоеЛицо,ОсновнойБанковскийСчет,ОсновнойБанковскийСчет/НомерСчета"
    url = "{app_url}//odata/standard.odata/Catalog_Организации?{format_odata}&$expand=ОсновнойБанковскийСчет&$select={company_keys}".format(
        app_url=app_url, format_odata=format_odata, company_keys=company_keys)

    response = requests.get(url, auth=credentials, allow_redirects=False)
    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию:')
        print(response.text)
        return False

    response = json.loads(response.text)
    if len(response['value']) == 0:
        print('Справочник Организации не имеет записей')
        return False

    return True


def check_odata_partners(app_url, user):
    print("Проверяем справочник Контрагенты")
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))
    format_odata = "$format=json;odata=nometadata"
    partner_keys = "Ref_Key,Description,ИНН,КПП,РегистрационныйНомер"
    partners_skip = 0
    partners_top = 5
    url = "{app_url}//odata/standard.odata/Catalog_Контрагенты?{format_odata}&$orderby=Description&$select={partner_keys}&$top={partners_top}&$skip={partners_skip}&$filter=not (IsFolder)".format(
        app_url=app_url,
        format_odata=format_odata,
        partner_keys=partner_keys,
        partners_skip=partners_skip,
        partners_top=partners_top)

    response = requests.get(url, auth=credentials, allow_redirects=False)
    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию:')
        print(response.text)
        return False

    response = json.loads(response.text)
    if len(response['value']) == 0:
        print('Справочник Контрагенты не имеет записей')
        return False

    return True


def check_odata_assortment(app_url, user):
    print("Проверяем справочник Номенклатура")
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))
    format_odata = "$format=json;odata=nometadata"
    item_keys = "Ref_Key,Description,НаименованиеПолное,ЕдиницаИзмерения/Code,ЕдиницаИзмерения/Description"
    items_skip = 0
    items_top = 5
    url = "{app_url}//odata/standard.odata/Catalog_Номенклатура?{format_odata}&$expand=ЕдиницаИзмерения&$orderby=Description&$select={item_keys}&$top={items_top}&$skip={items_skip}&$filter=not (IsFolder)".format(
        app_url=app_url,
        format_odata=format_odata,
        item_keys=item_keys,
        items_skip=items_skip,
        items_top=items_top)

    response = requests.get(url, auth=credentials, allow_redirects=False)
    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию:')
        print(response.text)
        return False

    response = json.loads(response.text)
    if len(response['value']) == 0:
        print('Справочник Номенклатура не имеет записей')
        return False

    return True


def check_odata_pricelist(app_url, user):
    print("Проверяем цены номенклатуры")
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))
    format_odata = "$format=json;odata=nometadata"
    item_keys = "Номенклатура/Description,Номенклатура/Ref_Key,Цена,ЦенаВключаетНДС,Валюта/Description,Валюта/Code"
    url = "{app_url}//odata/standard.odata/InformationRegister_ЦеныНоменклатурыДокументов?{format_odata}&$expand=Валюта,Номенклатура&$select={item_keys}".format(
        app_url=app_url,
        format_odata=format_odata,
        item_keys=item_keys)

    response = requests.get(url, auth=credentials, allow_redirects=False)
    if response.status_code != 200:
        print('Ответ не 200. Проверьте URL или авторизацию:')
        print(response.text)
        return False

    return True


# 4. Проверка DataTransfer


def check_data_transfer(app_url, user, enterprise_data_path):
    url = app_url + "/hs/dt/storage/integration/post/"
    credentials = HTTPBasicAuth(user.get('login'), user.get('password'))

    headers = {"IBSession": "start"}
    response = requests.post(url, auth=credentials, headers=headers, allow_redirects=False)
    put_location = response.headers.get('Location')
    put_cookie = response.headers.get('Set-Cookie')

    headers = {"Cookie": put_cookie, "IBSession": "finish"}

    with open(enterprise_data_path, 'rb') as enterprise_data:
        response = requests.put(put_location,
                                auth=credentials,
                                data=enterprise_data,
                                headers=headers,
                                allow_redirects=False)

    job_id = json.loads(response.text).get('result').get('id')

    headers = {"IBSession": "start"}
    url = app_url + "/hs/dt/storage/jobs/" + job_id

    response = requests.get(url, auth=credentials, headers=headers, allow_redirects=False)

    get_location = response.headers.get('Location')
    get_cookie = response.headers.get('Set-Cookie')

    headers = {"Cookie": get_cookie}
    app_stuffed = False

    while not app_stuffed:
        response = requests.get(get_location, auth=credentials, headers=headers, allow_redirects=False)
        status_code = json.loads(response.text).get('general').get('response')
        time.sleep(2)
        print(status_code)

        if status_code != 10202:
            app_stuffed = True

    job_status_code = json.loads(response.text).get('result')[0].get('response')
    if job_status_code != 10200:
        print('Не удалось загрузить файл enterprise data:')
        print(json.loads(response.text).get('result')[0].get('message'))
        # result_map.update({"Error": True, "Message": response.get('message')})
        return False


server = "https://1cfresh.com"
reg = "a/adm/hs/ext_api/execute"
# Имя пользователя и пароль владельца абонента.
username = "user1@yopmail.com"
password = "123Qwer"
# Номер области, с которой включается интеграция.
# Запрашивается у пользователя.
# Можно получить с помощью функции get_tenant_list()
tenant_id = 1
# Имя приложения с которым включается интеграция.
# Для БП это ea и ea_corp
app_name = 'ea'

# Путь к файлу для отправки в 1С. Данные должны быть валидны для конкретной области.
enterprise_data_path = 'bill_plan.zip'

credentials = (username, password)
app_url = "{server}/a/{app_name}/{tenant_id}".format(server=server, app_name=app_name, tenant_id=tenant_id)

# 1. Создаем пользователя.
# Внутри 4 последовательных запроса к МС.
# Результат: Новый пользователь привязанный к переданной области
#
# Внимание!
# Если создавать пользователя не нужно, то можно использовать уже созданного и пропустить этот шаг. Например:
# user = {"login": "new_name", "password": "123Qwer"}
#

print("1. Создаем пользователя для интеграции")
user = user_for_crm_integration(server, reg, credentials, tenant_id, "")
if user is None:
    exit(1)
print('1. Пользователь {user} успешно создан.'.format(user=user['login']))
print("")

# 2. Устанавливаем настройки через DataTransfer
# Устанавливаем настройки интеграции с CRM
# Результат: В области в справочнике e1cib/list/Справочник.НастройкиИнтеграцииCRM появляется новая запись
# Для пользователя открывается Odata
#
print("2. Установим настройки интеграции с CRM...")
time.sleep(10)
setup_integration(app_url, user)
print("2. Настройки интеграции установлены")
print("")

# 3. Проверяем OData для нового пользователя
# Делаем последовательные запросы через Odata, чтобы удостовериться, что все запросы используемые CRM работают
# Сломаться они могли из-за изменений в метаданных конфигурации
# Результат: Все запросы должны вернуть какой-то результат.
#

print('3. Проверим ODATA...')
time.sleep(10)
if not check_odata(app_url, user):
    print("Интерфейс OData не работает!")
    exit(1)
print('3. Проверка ODATA выполнена')
print("")

# 4. Отправляем данные в 1С
# Отправляем счет на оплату в область.
# Результат: В области должен появиться или измениться существующий счет.
# Документы: e1cib/list/Документ.СчетНаОплатуПокупателю
# В регистре должна e1cib/list/РегистрСведений.ДокументыИнтеграцииCRM появиться новая запись с этим счетом
# Описание сервиса отправки данных - https://its.1c.ru/db/fresh#content:19956672:hdoc
#

print('4. Проверим отправку данных через DataTransfer...')
time.sleep(10)
check_data_transfer(app_url, user, enterprise_data_path)
print('4. Проверка отправки данных через DataTransfer выполнена')
print("")

# 5. Изменить данные в 1С
# Необходимо изменить полученный счет в 1С. Можно изменить статус счета или любой реквизит.
# Результат: В регистре e1cib/list/РегистрСведений.ДокументыИнтеграцииCRM должна появиться запись с типом:
# Состояние = Подготовлено к отправке
#

# 6. Получить данные из 1С
# Необходимо запросить данные из 1С.
# Результат: Временный файл в котором содержится ED с реквизитами счета
# В 1С в регистре e1cib/list/РегистрСведений.ДокументыИнтеграцииCRM не должно быть записей с типом:
# Состояние = Подготовлено к отправке
# Описания сервиса получения данных - https://its.1c.ru/db/fresh#content:19956672:hdoc
# Запрос данных выполняется в скрипте CRM_confirm.py