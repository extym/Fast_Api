import datetime
import time
import requests
import json

#for production only
#requests.packages.urllib3.disable_warnings()

def read_image():
    for line in open('dict_images.json', 'r'):
        pages = json.loads(line)
    return pages


def write(smth):
    with open('log.txt', 'a') as file:
        how_time = datetime.datetime.now()
        file.write(str(how_time)+ '-' + smth)


def get_image(name, url):
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        with open("./images/" + name, "wb") as file:
            file.write(response.content)
    response.close()


pages = read_image()
print('from_pictures', len(pages))
for address in pages:  #[:10]:
    for key in address:
        if address.get(key) != [0]:
            print(address,    type(address))
            name, url = address[key]
            get_image(str(name), url)
            write(str(name))
            time.sleep(1)
        else:

            continue

    #write(name)
    print(name, url)

