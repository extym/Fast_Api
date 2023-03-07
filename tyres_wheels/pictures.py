import datetime
import time
import requests
import json

# for production only
requests.packages.urllib3.disable_warnings()

def read_image():
    for line in open('/usr/local/bin/fuck_debian/tyres_wheels/dict_images.json', 'r'):
        pages = json.loads(line)
    return pages


def write(smth):
    with open('/usr/local/bin/fuck_debian/tyres_wheels/log.txt', 'a') as file:
        how_time = datetime.datetime.now()
        file.write(str(how_time)+ '-' + smth)


def get_image(name, url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open("/home/ivanovka/data/www/1000koles.ru/pictures/" + name, "wb") as file:
        #with open("images/" + name, "wb") as file:
            file.write(response.content)
    response.close()


pages = read_image()
print('from_pictures', len(pages))
for address in pages:  #[:10]:
    for key in address:
        if address.get(key) != [0] and address[key][1] is not None:
            print(address,    type(address))
            name, url = address[key]
            get_image(str(name), url)
            write(str(name))
            time.sleep(1)
        else:
            continue

    #write(name)
    print(name, url)

