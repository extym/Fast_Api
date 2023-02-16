import pytz
import json
from xml.dom import minidom
from datetime import datetime
from read_json import processing_request, processing_json

# warehouses = {21405051875000: "Октябрьский малый", 23012928587000: "Октябрьский крупногабарит", 23138678478000: "Октябрьский новый крупногабаритный", 23990969841000: "Основной склад - Курьеры", 23997026419000: "Осн склад Курьеры некрупный груз до 25кг",
#               1020000039316000: "RFBS наш склад Деловые Линии", 1020000068495000: "НАША ДОСТАВКА Москва и МО", 1020000075732000: "RFBS наш склад СДЭК"}

warehouses = {'OZ.ОктМал': "Октябрьский малый",'OZ.ОктКГnew': "Октябрьский новый крупногабаритный",
              'OZ.ОснКурьер': "Основной склад - Курьеры",'OZ.ОснКурьердо25': "Осн склад Курьеры некрупный груз до 25кг",
                'OZ.RFBSнашсклДЛ': "RFBS наш склад Деловые Линии",'OZ.НашадостМиМО': "НАША ДОСТАВКА Москва и МО",
               'OZ.RFBSНашсклСДЭК' : "RFBS наш склад СДЭК", "OZ.ДостКГ": "Новая доставка Крупный груз"}


# wh_ozon = {'casual': [("Октябрьский малый", 21405051875000),("Осн склад Курьеры некрупный груз до 25кг", 23997026419000)],
#            'kgt': [("Октябрьский новый крупногабаритный", 23138678478000),("Основной склад - Курьеры", 23990969841000), ("RFBS наш склад Деловые Линии", 1020000039316000)],
#            'all': [("НАША ДОСТАВКА Москва и МО", 1020000068495000),("RFBS наш склад СДЭК", 1020000075732000)]
#            }

##for Test only
# wh_ozon = {'casual': [("Октябрьский малый", 21405051875000)]}
#
# wh_ozon_product = {'casual': ['OWLM200201', 'OWLM200300', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN50', 'ИМRUNN40', 'OWLM200302', 'OWLM200100', 'OWLM200301', 'OWLM200202', 'OWLT190301/2', 'OWLT190303/2', 'OWLT190402/2', 'OWLT190702/2', 'OWLT200901/2', 'OWLT190901/2', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'ИМALS80', 'OWLT190305'],
#            'kgt': ['OWLT190101', 'OWLT190302', 'OWLT190403S', 'OWLT190304', 'ИМOWLT190901', 'ИМOWLT200901', 'ИМMAL80', 'ИМHELLS65', 'ИМRUNN60', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200101', 'OWLM200102', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190303', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSS100', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190303', 'OWLT190402', 'OWLT190702', 'OWLT200901', 'OWLT190901', 'TOWLT190302', 'OWLT190201']
#            }
#
# another_id = {'OWLT190101': 'а0026033', 'OWLM200300': 'а0027568', 'OWLT190304': 'а0027470',
#               'OWLT190403S': 'а0027471', 'OWLT190101': 'а0026033'}

def check_wh(outlets):
    # print('outlets', outlets)
    proxy = []
    for outlet in outlets:
        re_outlets = warehouses.get(outlet)
        if re_outlets is not None:
            proxy.append(re_outlets)

    result = tuple(proxy)

    return result



def read_file():
    with open('prod_balances.json', 'r') as file:
        proxy_data = json.load(file)
        datas = proxy_data['result']
        return datas


def write_file(data):
    with open('target_data.json', 'w') as file:
        json.dump(data, file)


def get_need_data():
    with open('target.json', 'r') as file:
        data = json.load(file)
        #prod_data = data['result']['items']

    return data

def o_create():
    root = minidom.Document()

    # date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    date = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
    #print(date)
    xml_root = root.createElement('yml_catalog')
    root.appendChild(xml_root)
    xml_root.setAttribute('date', date)

    shopChild = root.createElement('shop')
    textName = root.createTextNode('ООО СТМ')
    offersChild = root.createElement('offers')

    def create_offer(offer_id, outlet, quantity):  #(offer_id, price, oldprice, min_price, outlet):

        offerChild = root.createElement('offer')
        offerChild.setAttribute('id', offer_id)
        #offerChild.setAttribute('id', f'162499{y}')
        offerChild.setAttribute('available', 'true')
        offersChild.appendChild(offerChild)

        # priceOfferChild = root.createElement('price')
        # textPriceOffer = root.createTextNode(price)
        # priceOfferChild.appendChild(textPriceOffer)
        # offerChild.appendChild(priceOfferChild)

        ##need if update price
        # oldpriceOfferChild = root.createElement('oldprice')
        # textOldPriceOffer = root.createTextNode(oldprice)
        # oldpriceOfferChild.appendChild(textOldPriceOffer)
        # offerChild.appendChild(oldpriceOfferChild)

        ##need if update price
        # min_priceOfferChild = root.createElement('min_price')
        # textMinPriceOffer = root.createTextNode(min_price)
        # min_priceOfferChild.appendChild(textMinPriceOffer)
        # offerChild.appendChild(min_priceOfferChild)

        outletsChild = root.createElement('outlets')

        for outlet_name in outlet:  #outlets:   #outlets -  maybe dictionary, where key=warehouse_id, value=warehouse_in_stock
            #print(outlet_name)
            outletOfferChild = root.createElement('outlet')
            outletOfferChild.setAttribute('instock', f'{quantity}')  #f'{outlets[key]}')
            outletOfferChild.setAttribute('warehouse_name', f'{outlet_name}')
            outletsChild.appendChild(outletOfferChild)

        offerChild.appendChild(outletsChild)


        # nameOfferChild = root.createElement('name')
        # textNameOffer = root.createTextNode(name)
        # nameOfferChild.appendChild(textNameOffer)
        # offerChild.appendChild(nameOfferChild)
        #
        # categoryIdOfferChild = root.createElement('categoryId')
        # textCategoryIdOffer = root.createTextNode(category_id)
        # categoryIdOfferChild.appendChild(textCategoryIdOffer)
        # offerChild.appendChild(categoryIdOfferChild)
        #
        # countOfferChild = root.createElement('count')
        # textcountOffer = root.createTextNode(count)
        # countOfferChild.appendChild(textcountOffer)
        # offerChild.appendChild(countOfferChild)
        #
        # minQuantityOfferChild = root.createElement('min-quantity')
        # textMinQuantityOffer = root.createTextNode('4')
        # minQuantityOfferChild.appendChild(textMinQuantityOffer)
        # offerChild.appendChild(minQuantityOfferChild)


    need_data = processing_json()  #get_need_data()
    #print(len(need_data), type(need_data))
    count = 0
    for value in need_data:  #our_data[10:]:
        #id_from_1c = value[0]
        offer_id = value[1]
        # if offer_id in another_id:
        #     offer_id = another_id[offer_id]
        outlets = check_wh(value[4])
        quantity = value[3]  # ???
        price = value[2]  #["Цена"]



        if offer_id != '' and quantity is not None:
            count += 1
            create_offer(str(offer_id), outlets, str(quantity))  #(offer_id, price, oldprice, min_price, outlet)

    #print('in xml', count, 'products')



    print(count)

    #create_offer(offer_id, price, oldprice, min_price, outlet)

    #
    # shopChild.appendChild(urlChild)
    # shopChild.appendChild(platformChild)
    # shopChild.appendChild(versionChild)
    # shopChild.appendChild(deliveryChild)
    # shopChild.appendChild(currenciesChild)
    # currenciesChild.appendChild(currencyChild)
    # shopChild.appendChild(outlets)
    shopChild.appendChild(offersChild)

    xml_root.appendChild(shopChild)

    xml_str = root.toprettyxml(indent="\t")
    #for development
    # save_path_file = "ozon_data.xml"
    #for production
    save_path_file = "/var/www/html/2c/ozon_data.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


#o_create()