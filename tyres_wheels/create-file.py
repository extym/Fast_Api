import json
import sys
from xml.dom import minidom
import datetime
from prepare_data_export import get_need_data, get_need_data_v2
# from copy_connect import check_and_write
from copy_connect import check_write_json, check_and_write_v3
from getcsv import standart_wheels_csv
from get_json import standart_wheels_from_json
from cred import DATA_IMG, DATA_PATH
from categories import categories_wheels, cats_wheels_upper, special_wheels

desk_carwel = 'Диски CARWEL- cовременный, динамично развивающийся бренд. Новейшее передовое оборудование и ' \
              'современные технологии по производству литых колесных дисков отвечающие самым высоким стандартам ' \
              'качества и надежности,является не единственным конкурентным преимуществом.'
# categories = {'iFree': 628, 'Carwel': 1969, 'KHOMEN': 1968, 'КиК': 1782, 'Скад': 1926}
need_cats = ['NEO', 'Wheels UP', 'iFree', 'CARWEL', 'КИК', 'Tech-Line', 'Carwel', 'RST', 'КиК', 'Venti', 'IFREE',
             'VENTI', 'TECH-LINE', 'СКАД', 'KHOMEN']

# ll = [i.upper() for i in need_cats]
# need_cats.extend(ll)
# print(7777, set(need_cats))

# check_and_write()


root = minidom.Document()

date = datetime.datetime.now(datetime.timezone.utc).isoformat()
xml_root = root.createElement('yml_catalog')
root.appendChild(xml_root)
xml_root.setAttribute('date', date)

productChild = root.createElement('shop')

nameChild = root.createElement('name')
textName = root.createTextNode('1000koles')
nameChild.appendChild(textName)

companyChild = root.createElement('company')
textCompany = root.createTextNode('ИП Иванов К.А')
companyChild.appendChild(textCompany)

urlChild = root.createElement('url')
textUrl = root.createTextNode('https://www.1000koles.ru')
urlChild.appendChild(textUrl)

platformChild = root.createElement('platform')
textPlatform = root.createTextNode('ShopCMS')
platformChild.appendChild(textPlatform)

versionChild = root.createElement('version')
textVersion = root.createTextNode('1.0')
versionChild.appendChild(textVersion)

# currenciesChild = root.createElement('currencies')

deliveryChild = root.createElement('delivery-options')

deliveryOptionChild = root.createElement('option')
deliveryOptionChild.setAttribute('cost', '0')
deliveryOptionChild.setAttribute('days', '3')
deliveryOptionChild.setAttribute('order-before', '13')
deliveryChild.appendChild(deliveryOptionChild)

categoriesChild = root.createElement('categories')

categoryChild = root.createElement('category')
categoryChild.setAttribute('id', '1')
textCategory = root.createTextNode('Литые диски')
categoryChild.appendChild(textCategory)
categoriesChild.appendChild(categoryChild)

for key in special_wheels.keys():
    category_vendor = key
    categories_id = special_wheels[category_vendor]
    categoryChild = root.createElement('category')
    categoryChild.setAttribute('id', f'{categories_id}')
    categoryChild.setAttribute('parentId', '1')
    textCategory = root.createTextNode(f'{category_vendor}')
    categoryChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryChild)

offersChild = root.createElement('offers')


def clean_standart_data():
    data = {}
    with open(DATA_PATH + 'standart_data.json', 'w') as f:
        json.dump(data, f)

    print('Clean standart data successfuly ')


def create_offer(name, vendor, product_code, category_id, description, url, count, price):
    offerChild = root.createElement('offer')
    offerChild.setAttribute('id', product_code)
    # offerChild.setAttribute('id', f'162499{y}')
    offerChild.setAttribute('available', 'true')
    offersChild.appendChild(offerChild)

    nameOfferChild = root.createElement('name')
    textNameOffer = root.createTextNode(name)
    nameOfferChild.appendChild(textNameOffer)
    offerChild.appendChild(nameOfferChild)

    vendorOfferChild = root.createElement('vendor')
    textVendorOffer = root.createTextNode(vendor)
    vendorOfferChild.appendChild(textVendorOffer)
    offerChild.appendChild(vendorOfferChild)

    vendorCodeOfferChild = root.createElement('vendorCode')
    textVendorCodeOffer = root.createTextNode(product_code)
    vendorCodeOfferChild.appendChild(textVendorCodeOffer)
    offerChild.appendChild(vendorCodeOfferChild)

    categoryIdOfferChild = root.createElement('categoryId')
    textCategoryIdOffer = root.createTextNode(category_id)
    categoryIdOfferChild.appendChild(textCategoryIdOffer)
    offerChild.appendChild(categoryIdOfferChild)

    pictureOfferChild = root.createElement('picture')
    textPictureOffer = root.createTextNode(url)
    pictureOfferChild.appendChild(textPictureOffer)
    offerChild.appendChild(pictureOfferChild)

    priceOfferChild = root.createElement('price')
    textPriceOffer = root.createTextNode(price)
    priceOfferChild.appendChild(textPriceOffer)
    offerChild.appendChild(priceOfferChild)

    descriptionOfferChild = root.createElement('description')
    textdescriptionOffer = root.createTextNode(description)
    descriptionOfferChild.appendChild(textdescriptionOffer)
    offerChild.appendChild(descriptionOfferChild)

    countOfferChild = root.createElement('count')
    textcountOffer = root.createTextNode(count)
    countOfferChild.appendChild(textcountOffer)
    offerChild.appendChild(countOfferChild)

    minQuantityOfferChild = root.createElement('min-quantity')
    textMinQuantityOffer = root.createTextNode('2')
    minQuantityOfferChild.appendChild(textMinQuantityOffer)
    offerChild.appendChild(minQuantityOfferChild)


# csv_data = standart_wheels_csv()
# json_data = standart_wheels_from_json()
# need_data = check_and_write_v3()


def create_need_data():
    csv_data = standart_wheels_csv()
    json_data = standart_wheels_from_json()
    data = check_and_write_v3()
    pre_csv_data = {key: value for key, value in csv_data.items() if int(value[0][4]) >= 4}
    pre_json_data = {k: v for k, v in json_data.items() if int(v[0][4]) >= 4}
    need_data = dict()
    for ke, val in data.items():
        if pre_json_data.get(ke):
            pre_count_json = pre_json_data.get(ke)
            count_json = int(pre_count_json[0][4])
            del pre_json_data[ke]
        else:
            count_json = 0
        if pre_csv_data.get(ke):
            pre_count_csv = pre_csv_data.get(ke)
            count_csv = int(pre_count_csv[0][4])
            del pre_csv_data[ke]
        else:
            count_csv = 0

        in_stok = int(val[0][4]) + count_json + count_csv
        new_data = val[0].copy()
        del new_data[4]
        new_data.insert(4, in_stok)

        need_data.update({ke: (new_data, val[1], val[2], val[3])})

    need_data.update(pre_csv_data)
    need_data.update(pre_json_data)
    print('ALL_RIDE create_need_data ', len(need_data))

    return need_data

# try:
need_data = create_need_data()
print('make_need_data_successfuly ', len(need_data))
# except:
#     with open(DATA_PATH + '/standart_data.json', 'r') as file:
#         need_data = json.load(file)
#         print('EXTEND_Fuck_UP_read_successfuly', len(need_data))
# #
# print('len_need_data_for_offers ', len(need_data))
counter = 0
row = tuple()
for row in need_data.values():
    try:
        if row[0][7] in need_cats and int(row[0][3]) > 7000 and row[0][4] >= 4 and row[3]:
            url = 'https://www.1000koles.ru/pictures/' + row[1][0]
            # if row[0][-1] == 'colrad':
            #     url = 'https://www.1000koles.ru/pictures/' + row[1][0]
            ## create_offer(name, vendor, product_code, category_id, description, url, count, price)
            create_offer(row[0][1], row[0][7], row[0][6], str(row[0][0]), row[0][2], url, str(row[0][4]),
                         str(row[0][3]))
            counter += 1
    except Exception as error:
        print('some_fuck_up_need_data {} {} {} {}'.format
              (error, type(row[0][4]), row[0][4], row))
        continue
        # sys.exit()
    # if row[0][-1] == 'colrad':
    #     print(1111111111, row)
    # else:
    #     continue
# print(122222222222, row)

print('len_offers ', datetime.datetime.now(), counter)

productChild.appendChild(nameChild)
productChild.appendChild(companyChild)
productChild.appendChild(urlChild)
productChild.appendChild(platformChild)
productChild.appendChild(versionChild)
productChild.appendChild(deliveryChild)
# productChild.appendChild(currenciesChild)
# currenciesChild.appendChild(currencyChild)
productChild.appendChild(categoriesChild)
productChild.appendChild(offersChild)

xml_root.appendChild(productChild)

xml_str = root.toprettyxml(indent="\t", encoding="UTF-8")

# save_path_file = "/home/ivanovka/data/www/1000koles.ru/pictures/yandex.xml"

with open(DATA_IMG + "yandex.xml", "wb") as f:
    f.write(xml_str)

with open(DATA_IMG + "sber.xml", "wb") as f:
    f.write(xml_str)

clean_standart_data()

print('len_offers_last ', datetime.datetime.now(), counter)
