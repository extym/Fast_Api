from avito import get_creds
from cred import LOCAL_MODE
import requests
import csv
import json
import  wget


url = 'https://zakazjpexpressru.amocrm.ru'


def send_smth(metod):
    creds = get_creds()
    access_token = creds.get('access_token')
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    link = url + metod
    answer = requests.get(link, headers=headers)
    data = answer.json()
    print(data)

    return answer.text

# send_smth('/api/v4/leads/custom_fields')
# send_smth('/api/v4/contacts/custom_fields')

if LOCAL_MODE:
    UPLOAD_FOLDER = './'
    PATH = './'
else:
    UPLOAD_FOLDER = '/var/www/html/load/'
    PATH = '/home/userbe/phone/'


ALLOWED = {'csv', 'xls', 'xlsx'}


# csv_link = 'https://baz-on.ru/export/c2335/60a99/jpexpress-parts.csv'
gmotors_link = 'https://baz-on.ru/export/c1950/125c0/gmotors-drom.csv'


def shorter_data(data, curr_name):
    proxy = []
    try:
        for row in data:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])

            proxy.append(row)
        # print('proxy', len(proxy))
        with open(UPLOAD_FOLDER + 'shortened_data.csv', 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            for row in proxy:
                writer.writerow(row)

        result = True

    except Exception as ex:
        result = False
        print("ERROR {}".format(ex))

    return result




def read_file_from_link(link):
    file_read = wget.download(link)
    # file_read = wget.download(link, out = UPLOAD_FOLDER +  "proxy.csv")
    with open(file_read, encoding='windows-1251') as file:
        reader = csv.reader(file, delimiter=';')
        proxy = []
        for row in reader:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])
            proxy.append(row)
        print('proxy', len(proxy))
    with open(UPLOAD_FOLDER + 'gmotors-autowrite.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in proxy:
            writer.writerow(row)
            if len(row) > 50:
                print('ERROR_ROW', len(row))
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))



def read_eurozapchastspb_link():
    eurozapchastspb_link = 'https://eurozapchastspb.ru/files/autoru.csv'
    file_read = wget.download(eurozapchastspb_link)
    with open(file_read, encoding='windows-1251') as file:
        reader = csv.reader(file, delimiter=';')
        proxy = []
        for row in reader:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])
            proxy.append(row)
        print('proxy', len(proxy))
    with open(UPLOAD_FOLDER + 'eurozapchastspb-autowrite.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in proxy:
            writer.writerow(row)
            if len(row) > 50:
                print('ERROR_ROW', len(row))
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))

# read_eurozapchastspb_link()


def read_gmotors_link():
    gmotors_link = 'https://baz-on.ru/export/c1950/125c0/gmotors-drom.csv'
    file_read = wget.download(gmotors_link)
    # file_read = wget.download(link, out = UPLOAD_FOLDER +  "proxy.csv")
    with open(file_read, encoding='windows-1251') as file:
        reader = csv.reader(file, delimiter=';')
        proxy = []
        for row in reader:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])
            proxy.append(row)
        print('proxy', len(proxy))
    with open(UPLOAD_FOLDER + 'gmotors-autowrite.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in proxy:
            writer.writerow(row)
            if len(row) > 50:
                print('ERROR_ROW', len(row))
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))

# read_file_from_link(csv_link)
# read_gmotors_link()

def read_file():
    with open('/home/extym/develop/3431/prises/autoru.csv', encoding='windows-1251') as  file:
    # with open('gmotors-drom.csv', encoding='windows-1251') as  file:
    # with open('convert-xml-csv.csv', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        proxy = []
        for row in reader:
            for i in range(len(row)):
                if len(row[i]) > 250:
                    new = row.pop(i)
                    row.insert(i, new[:250])

            proxy.append(row)
        print('proxy', len(proxy))
    with open('autoru-rewrite.csv', 'w', encoding='windows-1251') as f:
    # with open('gmotors-rewrite-2.csv', 'w', encoding='windows-1251') as f:
    # with open('convert-xml-rewrite.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in proxy:
            writer.writerow(row)
            if len(row) > 50:
                print('ERROR_ROW', len(row))
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))


# read_file()

fildnames = ['title', 'price', 'manufacturer', 'state', 'manufactureNumber', 'description', 'frontRear', 'leftRight', 'deliveryCost', 'compatibility', 'condition', 'photoUrls', 'car', 'id', 'marking', 'color', 'analogsNumbers', 'partname']

def read_json_out_scv():
    with open('xmltojson.txt', 'r', encoding='utf-8') as file:
        data = json.load(file)
        need_data = data['parts']['part']
        # print(len(data['parts']))
        proxy = []
        # for row in need_data:
        #     # print(row)
        #     # break
        #     for i in range(len(row)):
        #         if len(row[i]) > 250:
        #             new = row.pop(i)
        #             row.insert(i, new[:250])

        #     proxy.append(row)
        # print('proxy', len(proxy))
    # with open('gmotors-rewrite-2.csv', 'w', encoding='windows-1251') as f:
    with open('xml-json-rewrite.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fildnames)
        for row in need_data:
            writer.writerow(row)
            if len(row) > 50:
                print('ERROR_ROW', len(row))
            for line in row:
                if len(line) > 250:
                    print('ERROR', len(line))


# read_json_out_scv()

import pandas as pd
import csv
def read_xls(file):
    data = pd.read_excel(files)
    # file = pd.read_excel('example.xlsx')
    df = pd.DataFrame(data).values
    proxy = {}
    for row in df:
        proxy[row[0]] = int(row[2])
    # print(type(proxy))

    return proxy


def read_price():
    file = open('file_price.csv', 'r')
    reader = csv.reader(file)
    data = []
    for row in reader:
        data.append(row[:6])

    return json.dumps(data)






# read_xls()