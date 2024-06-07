from project import DATA_PATH

import datetime
import time
import requests
import json
import urllib3

# for production only
requests.packages.urllib3.disable_warnings()



def rewrite_pictures_data(listt):

    with open(DATA_PATH + '/dict_images.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_images_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/dict_images.json', "w") as write_file:
        data_list.extend(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_images_write_1', len(listt))

    print('file_images_rewrite', len(data_list))


def rewrite_standart_data(listt):
    with open(DATA_PATH + '/standart_data.json', "r") as read_file:
        data_list = json.load(read_file)
        print('file_standart_data_read', len(data_list))
        read_file.close()

    with open(DATA_PATH + '/standart_data.json', "w") as write_file:
        # data_list.extend(listt)
        data_list.update(listt)
        json.dump(data_list, write_file)
        write_file.close()
        print('file_standart_data_write_1', len(listt))

    print('file_standart_data_rewrite', len(data_list))



def read_image_address():
    pages = None
    try:
        for line in open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', 'r'):
            pages = json.loads(line)
    except:
        for line in open('dict_images.json', 'r'):
            pages = json.loads(line)

    return pages


def write(smth):
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time)+ '-' + smth)
    except:
        with open('log.txt', 'a') as file:
            how_time = datetime.datetime.now()
            file.write(str(how_time) + '-' + smth)



def get_image(name, url):
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            with open(PHOTO_DIR + name, "wb") as file:
                file.write(response.content)
        response.close()
    except:
        print('some_fuck_up_get_image', name, url)


def dowload_images():
    pages = read_image_address()
    print('from_pictures', len(pages))
    count = len(pages)
    for address in pages:  #[:10]:
        for key in address:
            if address.get(key) != [0] and \
                    address[key][1] is not None and \
                    address[key][1] != '':
                count -= 1
                name, url = address[key]
                get_image(str(name), url)
                # write(str(name))
                print('get_image',count, name, url)
                time.sleep(1)
            else:
                continue
    for _ in range(30):
        print('We are sleep & wait clean')
        time.sleep(1)
    clean()


def clean():
    listt = []
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as file:
            json.dump(listt, file)

    except:
        with open('dict_images.json', "w") as file:
            json.dump(listt, file)

    print('clean_file-len_list',  len(listt))

# clean()
# dowload_images()