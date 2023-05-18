import datetime
import time
import requests
import json

# for production only
requests.packages.urllib3.disable_warnings()

def read_image():
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
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        try:
            with open("/home/ivanovka/data/www/1000koles.ru/pictures/" + name, "wb") as file:
                file.write(response.content)
        except:
            with open("images/" + name, "wb") as file:
                file.write(response.content)
    response.close()


pages = read_image()
print('from_pictures', len(pages))
for address in pages:  #[:10]:
    for key in address:
        if address.get(key) != [0] and address[key][1] is not None:
            #print('address', address)
            name, url = address[key]
            get_image(str(name), url)
            write(str(name))
            print('get_image', name, url)
            time.sleep(1)
        else:
            continue



listt = []
# try:
#     with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as file:
#         json.dump(listt, file)
# except:
#     with open('dict_images.json', "w") as file:
#         json.dump(listt, file)

def clean():
    listt = []
    try:
        with open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', "w") as file:
            json.dump(listt, file)
    except:
        with open('dict_images.json', "w") as file:
            json.dump(listt, file)

    print('clean_file-len_list',  len(listt))

clean()