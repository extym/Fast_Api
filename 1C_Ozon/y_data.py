import pytz

from xml.dom import minidom
from datetime import datetime
from read_json import processing_request, processing_json


category_parent = {'Строительство и ремонт': 1, "Товары для дома": 2}
category_par = { 'Сантехника': 2,  "Мебель": 5, 'Интерьер': 7}
category_p = {'Унитазы, писсуары, биде': 2, 'Унитазы, писсуары, биде': 2, "Раковины, пьедесталы": 4,
              "Шкафы, тумбы, комоды": 156, 'Комплектующие': 33, 'Готовые комплекты': 158, 'Зеркала': 171}
categories = { "Бачки для унитазов": 1122, "Шкафы": 1565, 'Тумбы': 1564}

another_id = {'OWLT190101': 'а0026033', 'OWLM200300': 'а0027568', 'OWLT190304': 'а0027470',
              'OWLT190403S': 'а0027471', 'OWLT190302': 'а0026027'}



# 	ID магазина: (ID склада, wh_from_1C, model)
wh_yandex= {658505: (50639, 'YM.СТМ', 'FBS'), 32268653: (432708, 'YM.СклЭкспресс', 'FBS_express'), 39191045: (479988, 'YM.НашадостСклОкт', 'DBS')}


def create_dbs():
    root = minidom.Document()

    # date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    date = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    #
    #print(date)
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', date)

    productChild = root.createElement('shop')

    nameChild = root.createElement('name')
    textName = root.createTextNode('OOO CTM')
    nameChild.appendChild(textName)

    companyChild = root.createElement('company')
    textCompany = root.createTextNode('OOO "CTM"')
    companyChild.appendChild(textCompany)

    urlChild = root.createElement('url')
    textUrl = root.createTextNode('https://owl1975.ru')
    urlChild.appendChild(textUrl)

    platformChild = root.createElement('platform')
    textPlatform = root.createTextNode('HostCMS')
    platformChild.appendChild(textPlatform)

    versionChild = root.createElement('version')
    textVersion = root.createTextNode('1.0')
    versionChild.appendChild(textVersion)

    #currenciesChild = root.createElement('currencies')

    deliveryOptionsChild = root.createElement('delivery-options')

    deliveOptionChild = root.createElement('option')
    deliveOptionChild.setAttribute('cost', '0')
    deliveOptionChild.setAttribute('days', '3')
    deliveOptionChild.setAttribute('order-before', '13')
    deliveryOptionsChild.appendChild(deliveOptionChild)

    pickupChild = root.createElement('pickup-options')

    pickupOptionChild = root.createElement('option')
    pickupOptionChild.setAttribute('cost', '0')
    pickupOptionChild.setAttribute('days', '1')
    pickupOptionChild.setAttribute('order-before', '13')
    pickupChild.appendChild(pickupOptionChild)

    ##For add product only? custom:111
    # categoriesChild = root.createElement('categories')
    #
    # categoryChild = root.createElement('category')
    # categoryChild.setAttribute('id', '1')
    # textCategory = root.createTextNode('Строительство и ремонт')
    # categoryChild.appendChild(textCategory)
    # categoriesChild.appendChild(categoryChild)
    #
    # categoryChild = root.createElement('category')
    # categoryChild.setAttribute('id', '2')
    # textCategory = root.createTextNode('Товары для дома')
    # categoryChild.appendChild(textCategory)
    # categoriesChild.appendChild(categoryChild)
    #
    # for key in categories.keys():
    #     category_vendor = key
    #     categories_id = categories[category_vendor]
    #     categoryChild = root.createElement('category')
    #     categoryChild.setAttribute('id', f'{categories_id}')
    #     categoryChild.setAttribute('parentId', '1')
    #     textCategory = root.createTextNode(f'{category_vendor}')
    #     categoryChild.appendChild(textCategory)
    #     categoriesChild.appendChild(categoryChild)


    offersChild = root.createElement('offers')
    def create_offer(product_code, count):  #(name, vendor, product_code, category_id, description,  url, count, price)

        offerChild = root.createElement('offer')
        offerChild.setAttribute('id', product_code)
        #offerChild.setAttribute('id', f'162499{y}')
        offerChild.setAttribute('available', 'true')
        offersChild.appendChild(offerChild)

        # nameOfferChild = root.createElement('name')
        # textNameOffer = root.createTextNode(name)
        # nameOfferChild.appendChild(textNameOffer)
        # offerChild.appendChild(nameOfferChild)

        # vendorOfferChild = root.createElement('vendor')
        # textVendorOffer = root.createTextNode(vendor)
        # vendorOfferChild.appendChild(textVendorOffer)
        # offerChild.appendChild(vendorOfferChild)

        vendorCodeOfferChild = root.createElement('vendorCode')
        textVendorCodeOffer = root.createTextNode(product_code)
        vendorCodeOfferChild.appendChild(textVendorCodeOffer)
        offerChild.appendChild(vendorCodeOfferChild)

        # priceOfferChild = root.createElement('price')
        # textPriceOffer = root.createTextNode(price)
        # priceOfferChild.appendChild(textPriceOffer)
        # offerChild.appendChild(priceOfferChild)

        deliveryOfferChild = root.createElement('delivery')
        textMinQuantityOffer = root.createTextNode('true')
        deliveryOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(deliveryOfferChild)

        pickupOfferChild = root.createElement('pickup')
        textMinQuantityOffer = root.createTextNode('true')
        pickupOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(pickupOfferChild)

        countOfferChild = root.createElement('count')
        textcountOffer = root.createTextNode(count)
        countOfferChild.appendChild(textcountOffer)
        offerChild.appendChild(countOfferChild)


    need_data = processing_json()
    print(type(need_data), len(need_data))
    cnt = 0
    for row in need_data:
        if 'YM.НашадостСклОкт' in row[4]:
            count = row[3]
            if count is None:
                count = 0
            product_code = row[1]
            if product_code in another_id:
                product_code = another_id[product_code]
            if product_code != '':
                create_offer(product_code, str(count))  #(name, vendor, product_code, category_id, description,  url, count, price)
                cnt += 1
    print('row00000', row)
    print('cnt', cnt)

    productChild.appendChild(nameChild)
    productChild.appendChild(companyChild)
    productChild.appendChild(urlChild)
    productChild.appendChild(platformChild)
    productChild.appendChild(versionChild)
    productChild.appendChild(deliveryOptionsChild)
    productChild.appendChild(pickupChild)
    # productChild.appendChild(currenciesChild)
    # currenciesChild.appendChild(currencyChild)
    #productChild.appendChild(categoriesChild)
    productChild.appendChild(offersChild)

    xml_root.appendChild(productChild)

    xml_str = root.toprettyxml(indent="\t")
    #for development
    # save_path_file = "yandex-dbs.xml"
    #for production
    save_path_file = "/var/www/html/2c/yandex-dbs.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)



def create_fbs():
    root = minidom.Document()

    # date = datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat()
    date = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', date)

    productChild = root.createElement('shop')

    nameChild = root.createElement('name')
    textName = root.createTextNode('OOO CTM')
    nameChild.appendChild(textName)

    companyChild = root.createElement('company')
    textCompany = root.createTextNode('OOO "CTM"')
    companyChild.appendChild(textCompany)

    urlChild = root.createElement('url')
    textUrl = root.createTextNode('https://owl1975.ru')
    urlChild.appendChild(textUrl)

    platformChild = root.createElement('platform')
    textPlatform = root.createTextNode('HostCMS')
    platformChild.appendChild(textPlatform)

    versionChild = root.createElement('version')
    textVersion = root.createTextNode('1.0')
    versionChild.appendChild(textVersion)

    #currenciesChild = root.createElement('currencies')

    deliveryOptionsChild = root.createElement('delivery-options')

    deliveOptionChild = root.createElement('option')
    deliveOptionChild.setAttribute('cost', '0')
    deliveOptionChild.setAttribute('days', '3')
    deliveOptionChild.setAttribute('order-before', '13')
    deliveryOptionsChild.appendChild(deliveOptionChild)

    pickupChild = root.createElement('pickup-options')

    pickupOptionChild = root.createElement('option')
    pickupOptionChild.setAttribute('cost', '0')
    pickupOptionChild.setAttribute('days', '1')
    pickupOptionChild.setAttribute('order-before', '13')
    pickupChild.appendChild(pickupOptionChild)

    offersChild = root.createElement('offers')
    def create_offer(product_code, count):  #(name, vendor, product_code, category_id, description,  url, count, price)

        offerChild = root.createElement('offer')
        offerChild.setAttribute('id', product_code)
        #offerChild.setAttribute('id', f'162499{y}')
        offerChild.setAttribute('available', 'true')
        offersChild.appendChild(offerChild)

        # vendorOfferChild = root.createElement('vendor')
        # textVendorOffer = root.createTextNode(vendor)
        # vendorOfferChild.appendChild(textVendorOffer)
        # offerChild.appendChild(vendorOfferChild)

        vendorCodeOfferChild = root.createElement('vendorCode')
        textVendorCodeOffer = root.createTextNode(product_code)
        vendorCodeOfferChild.appendChild(textVendorCodeOffer)
        offerChild.appendChild(vendorCodeOfferChild)

        # categoryIdOfferChild = root.createElement('categoryId')
        # textCategoryIdOffer = root.createTextNode(category_id)
        # categoryIdOfferChild.appendChild(textCategoryIdOffer)
        # offerChild.appendChild(categoryIdOfferChild)

        # priceOfferChild = root.createElement('price')
        # textPriceOffer = root.createTextNode(price)
        # priceOfferChild.appendChild(textPriceOffer)
        # offerChild.appendChild(priceOfferChild)

        deliveryOfferChild = root.createElement('delivery')
        textMinQuantityOffer = root.createTextNode('true')
        deliveryOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(deliveryOfferChild)

        pickupOfferChild = root.createElement('pickup')
        textMinQuantityOffer = root.createTextNode('true')
        pickupOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(pickupOfferChild)

        countOfferChild = root.createElement('count')
        textcountOffer = root.createTextNode(count)
        countOfferChild.appendChild(textcountOffer)
        offerChild.appendChild(countOfferChild)


    need_data = processing_json()
    print(type(need_data), len(need_data))
    cnt = 0
    for row in need_data:
        if 'YM.СТМ' in row[4]:
            count = row[3]
            if count is None:
                count = 0
            product_code = row[1]
            if product_code in another_id:
                product_code = another_id[product_code]
            if product_code != '':
                create_offer(product_code, str(count))  #(name, vendor, product_code, category_id, description,  url, count, price)
                cnt += 1
    print('rowYM.СТМ', row)
    print('cnt', cnt)


    productChild.appendChild(nameChild)
    productChild.appendChild(companyChild)
    productChild.appendChild(urlChild)
    productChild.appendChild(platformChild)
    productChild.appendChild(versionChild)
    productChild.appendChild(deliveryOptionsChild)
    productChild.appendChild(pickupChild)
    # productChild.appendChild(currenciesChild)
    # currenciesChild.appendChild(currencyChild)

    ##For add product only? custom:111
    #productChild.appendChild(categoriesChild)
    productChild.appendChild(offersChild)

    xml_root.appendChild(productChild)

    xml_str = root.toprettyxml(indent="\t")
    #for development
    # save_path_file = "yandex-fbs.xml"
    #for production
    save_path_file = "/var/www/html/2c/yandex-fbs.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


def create_expresso():
    root = minidom.Document()

    # date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    date = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    #print(date)
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', date)

    productChild = root.createElement('shop')

    nameChild = root.createElement('name')
    textName = root.createTextNode('OOO CTM')
    nameChild.appendChild(textName)

    companyChild = root.createElement('company')
    textCompany = root.createTextNode('OOO "CTM"')
    companyChild.appendChild(textCompany)

    urlChild = root.createElement('url')
    textUrl = root.createTextNode('https://owl1975.ru')
    urlChild.appendChild(textUrl)

    platformChild = root.createElement('platform')
    textPlatform = root.createTextNode('HostCMS')
    platformChild.appendChild(textPlatform)

    versionChild = root.createElement('version')
    textVersion = root.createTextNode('1.0')
    versionChild.appendChild(textVersion)

    #currenciesChild = root.createElement('currencies')

    deliveryOptionsChild = root.createElement('delivery-options')

    deliveOptionChild = root.createElement('option')
    deliveOptionChild.setAttribute('cost', '0')
    deliveOptionChild.setAttribute('days', '3')
    deliveOptionChild.setAttribute('order-before', '13')
    deliveryOptionsChild.appendChild(deliveOptionChild)

    pickupChild = root.createElement('pickup-options')

    pickupOptionChild = root.createElement('option')
    pickupOptionChild.setAttribute('cost', '0')
    pickupOptionChild.setAttribute('days', '1')
    pickupOptionChild.setAttribute('order-before', '13')
    pickupChild.appendChild(pickupOptionChild)

    offersChild = root.createElement('offers')
    def create_offer(product_code, count):  #(name, vendor, product_code, category_id, description,  url, count, price)

        offerChild = root.createElement('offer')
        offerChild.setAttribute('id', product_code)
        #offerChild.setAttribute('id', f'162499{y}')
        offerChild.setAttribute('available', 'true')
        offersChild.appendChild(offerChild)

        # nameOfferChild = root.createElement('name')
        # textNameOffer = root.createTextNode(name)
        # nameOfferChild.appendChild(textNameOffer)
        # offerChild.appendChild(nameOfferChild)

        # vendorOfferChild = root.createElement('vendor')
        # textVendorOffer = root.createTextNode(vendor)
        # vendorOfferChild.appendChild(textVendorOffer)
        # offerChild.appendChild(vendorOfferChild)

        vendorCodeOfferChild = root.createElement('vendorCode')
        textVendorCodeOffer = root.createTextNode(product_code)
        vendorCodeOfferChild.appendChild(textVendorCodeOffer)
        offerChild.appendChild(vendorCodeOfferChild)

        # categoryIdOfferChild = root.createElement('categoryId')
        # textCategoryIdOffer = root.createTextNode(category_id)
        # categoryIdOfferChild.appendChild(textCategoryIdOffer)
        # offerChild.appendChild(categoryIdOfferChild)

        # pictureOfferChild = root.createElement('picture')
        # textPictureOffer = root.createTextNode(url)
        # pictureOfferChild.appendChild(textPictureOffer)
        # offerChild.appendChild(pictureOfferChild)


        # priceOfferChild = root.createElement('price')
        # textPriceOffer = root.createTextNode(price)
        # priceOfferChild.appendChild(textPriceOffer)
        # offerChild.appendChild(priceOfferChild)

        # descriptionOfferChild = root.createElement('description')
        # textdescriptionOffer = root.createTextNode(description)
        # descriptionOfferChild.appendChild(textdescriptionOffer)
        # offerChild.appendChild(descriptionOfferChild)

        deliveryOfferChild = root.createElement('delivery')
        textMinQuantityOffer = root.createTextNode('true')
        deliveryOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(deliveryOfferChild)

        pickupOfferChild = root.createElement('pickup')
        textMinQuantityOffer = root.createTextNode('true')
        pickupOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(pickupOfferChild)

        countOfferChild = root.createElement('count')
        textcountOffer = root.createTextNode(count)
        countOfferChild.appendChild(textcountOffer)
        offerChild.appendChild(countOfferChild)


    need_data = processing_json()
    #print(type(need_data), len(need_data))
    cnt = 0
    for row in need_data:
        if 'YM.СклЭкспресс' in row[4]:
            count = row[3]
            if count is None:
                count = 0
            product_code = row[1]
            if product_code in another_id:
                product_code = another_id[product_code]
            if product_code != '':
                create_offer(product_code, str(count))  #(name, vendor, product_code, category_id, description,  url, count, price)
                cnt += 1

    print('row_for_YM.СклЭкспресс', row)
    print('cnt', cnt)

    productChild.appendChild(nameChild)
    productChild.appendChild(companyChild)
    productChild.appendChild(urlChild)
    productChild.appendChild(platformChild)
    productChild.appendChild(versionChild)
    productChild.appendChild(deliveryOptionsChild)
    productChild.appendChild(pickupChild)
    # productChild.appendChild(currenciesChild)
    # currenciesChild.appendChild(currencyChild)

    ##For add product only? custom:111
    #productChild.appendChild(categoriesChild)
    productChild.appendChild(offersChild)

    xml_root.appendChild(productChild)

    xml_str = root.toprettyxml(indent="\t")
    #for development
    # save_path_file = "yandex-exp.xml"
    #for production
    save_path_file = "/var/www/html/2c/yandex-exp.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


# create_dbs()
# create_fbs()
# create_expresso()