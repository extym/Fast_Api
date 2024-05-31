import datetime
import json
from xml.dom import minidom


def create_sber_xml(stocks_is_null=False, without_db=False, addons=False):
    root = minidom.Document()

    date = datetime.datetime.now().replace(second=0, microsecond=0)
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', str(date)[:-3])

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

    # currenciesChild = root.createElement('currencies')

    deliveryChild = root.createElement('shipment-options')

    deliveryOptionChild = root.createElement('option')
    # deliveryOptionChild.setAttribute('cost', '0')
    deliveryOptionChild.setAttribute('days', '2')
    deliveryOptionChild.setAttribute('order-before', '13')
    deliveryChild.appendChild(deliveryOptionChild)

    categoriesChild = root.createElement('categories')

    # < categories >
    # < category id = "1" > Все товары < / category >
    # < category id = "2"  parentId = "1" > Авто < / category >
    # < category id = "207" parentId = "2" > Шины и диски < / category >

    categoryAllChild = root.createElement('category')
    categoryAllChild.setAttribute('id', '1')
    textCategory = root.createTextNode('Все товары')
    categoryAllChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryAllChild)

    categoryAutoChild = root.createElement('category')
    categoryAutoChild.setAttribute('id', '2')
    categoryAutoChild.setAttribute('parentId', '1')
    textCategory = root.createTextNode('Авто')
    categoryAutoChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryAutoChild)

    categoryTWChild = root.createElement('category')
    categoryTWChild.setAttribute('id', '3')
    categoryTWChild.setAttribute('parentId', '2')
    textCategory = root.createTextNode('Шины и диски')
    categoryTWChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryTWChild)

    categoryChild = root.createElement('category')
    categoryChild.setAttribute('id', '4')
    categoryChild.setAttribute('parentId', '3')
    textCategory = root.createTextNode('Расходники')
    categoryChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryChild)

    categoryChild = root.createElement('category')
    categoryChild.setAttribute('id', '5')
    categoryChild.setAttribute('parentId', '3')
    textCategory = root.createTextNode('Литые диски')
    categoryChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryChild)

    for key in special_wheels.keys():
        category_vendor = key
        categories_id = special_wheels[category_vendor]
        categoryChild = root.createElement('category')
        categoryChild.setAttribute('id', f'{categories_id}')
        categoryChild.setAttribute('parentId', '5')
        textCategory = root.createTextNode(f'{category_vendor}')
        categoryChild.appendChild(textCategory)
        categoriesChild.appendChild(categoryChild)

    offersChild = root.createElement('offers')

    def create_offer(name, vendor, product_code, category_id, description, url, count, price):
        offer_id = vendor + product_code
        offerChild = root.createElement('offer')
        offerChild.setAttribute('id', offer_id)
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

        outletsChild = root.createElement('outlets')
        oneOutletChild = root.createElement('outlet')
        oneOutletChild.setAttribute('id', 'Склад мерчанта 1000koles.ru')
        oneOutletChild.setAttribute('instock', f"{count}")
        outletsChild.appendChild(oneOutletChild)
        offerChild.appendChild(outletsChild)

        descriptionOfferChild = root.createElement('description')
        textdescriptiontOffer = root.createTextNode(description)
        descriptionOfferChild.appendChild(textdescriptiontOffer)
        offerChild.appendChild(descriptionOfferChild)

        minQuantityOfferChild = root.createElement('min-quantity')
        textMinQuantityOffer = root.createTextNode('4')
        minQuantityOfferChild.appendChild(textMinQuantityOffer)
        offerChild.appendChild(minQuantityOfferChild)

    def create_need_data(without_db=False):
        json_data, csv_data = {}, {}
        if not without_db:
            try:
                csv_data = standart_wheels_csv()
            except:
                print("We don't get csv")
            try:
                json_data = standart_wheels_from_json()
            except:
                print("We don't get json")
            data = check_and_write_v4()
        else:
            try:
                csv_data = standart_wheels_csv(without_db=True)
            except:
                pass
            try:
                json_data = standart_wheels_from_json(without_db=True)
            except:
                pass


            data = standart_product_v2(get_new_pages_v2())

        pre_csv_data = {key: value for key, value in csv_data.items() if int(value[0][4]) >= 4}
        pre_json_data = {k: v for k, v in json_data.items() if int(v[0][4]) >= 4}
        need_data = dict()
        for ke, val in data.items():
            pre_count_json = pre_json_data.get(ke)
            if pre_count_json:
                count_json = int(pre_count_json[0][4])
            else:
                count_json = 0
                # print(111, ke, type(val[0][4]), val[0][4])
            pre_count_csv = pre_csv_data.get(ke)
            if pre_count_csv:
                count_csv = int(pre_count_csv[0][4])
            else:
                count_csv = 0
                # print(222, ke, type(val[0][4]), val[0][4])
            in_stok = int(val[0][4]) + count_json + count_csv
            new_data = val[0].copy()
            del new_data[4]
            new_data.insert(4, in_stok)
            need_data.update({ke: (new_data, val[1], val[2], val[3], val[4])})
        print('ALL_RIDE create_need_data ', len(need_data))

        return need_data

    try:
        need_data = create_need_data(without_db=without_db)
        print('MAKE_NEED_data_successfuly ', len(need_data))
    except:
        with open(DATA_PATH + '/standart_data.json', 'r') as file:
            need_data = json.load(file)

    print('len_need_data_for_offers ', len(need_data))
    counter = 0

    for row in need_data.values():
        try:
            if not stocks_is_null:
                if row[0][7] in need_cats and int(row[0][3]) > 6000 and row[0][4] >= 4 and row[3]:
                    url = 'https://www.1000koles.ru/pictures/' + row[1][0]
                    # price = int(row[0][3]) * 1.15
                    ## create_offer(name, vendor, product_code, category_id, description, url, count, price)
                    create_offer(row[0][1], row[0][7], row[0][6], str(row[0][0]), row[0][2], url, str(row[0][4]),
                                 str(row[0][3]))
                    counter += 1
            else:
                if row[0][7] in need_cats and int(row[0][3]) > 6000 and row[3]:
                    url = 'https://www.1000koles.ru/pictures/' + row[1][0]
                    # price = int(row[0][3]) * 1.15
                    shop_price = int(row[4]) * 1.32
                    ## create_offer(name, vendor, product_code, category_id, description, url, count, price)
                    create_offer(row[0][1], row[0][7], row[0][6], str(row[0][0]), row[0][2], url, "0", str(round(shop_price, 0)))
                    counter += 1
                    # print(555, row)
        except Exception as error:
            print('some_fuck_up_need_sb_data {} {} {}'
                  .format(error, row[0][4], row))
            continue
            # sys.exit()

    if addons:
        val_data = standart_addons_from_json(without_db=True, data=ventil_LS)
        # val_data = add_data.values()

        create_offer(val_data[0][1], val_data[0][7], val_data[0][6], str(val_data[0][0]), val_data[0][2],
                     val_data[1][1], str(val_data[0][4]), "25.0")
        counter += 1

    print('len_offers ', datetime.datetime.now(), counter)

    productChild.appendChild(nameChild)
    productChild.appendChild(companyChild)
    productChild.appendChild(urlChild)
    # productChild.appendChild(platformChild)
    # productChild.appendChild(versionChild)
    productChild.appendChild(deliveryChild)
    # productChild.appendChild(currenciesChild)
    # currenciesChild.appendChild(currencyChild)
    productChild.appendChild(categoriesChild)
    productChild.appendChild(offersChild)

    xml_root.appendChild(productChild)

    xml_str = root.toprettyxml(indent="\t", encoding="UTF-8")

    with open(DATA_IMG + "sber.xml", "wb") as f:
        f.write(xml_str)

    # clean_standart_data()
    # dowload_images() #TODO uncomment for production

    print('len_offers_last ', datetime.datetime.now(), counter)



create_sber_xml(stocks_is_null=True, without_db=True)
# create_sber_xml()
