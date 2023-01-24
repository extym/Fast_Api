from xml.dom import minidom
import datetime
from read_json import processing_request, processing_json



# desk_carwel = 'Диски CARWEL- cовременный, динамично развивающийся бренд. Новейшее передовое оборудование и современные технологии по производству литых колесных дисков отвечающие самым высоким стандартам качества и надежности,является не единственным конкурентным преимуществом.'
# categories = { 'iFree' : 628, 'Carwel' : 1969,  'KHOMEN' : 1968,  'КиК' : 1782 , 'Скад'  : 1926}
category_parent = {'Строительство и ремонт': 1, "Товары для дома": 2}
category_par = { 'Сантехника': 2,  "Мебель": 5, 'Интерьер': 7}
category_p = {'Унитазы, писсуары, биде': 2, 'Унитазы, писсуары, биде': 2, "Раковины, пьедесталы": 4,
              "Шкафы, тумбы, комоды": 156, 'Комплектующие': 33, 'Готовые комплекты': 158, 'Зеркала': 171}
categories = { "Бачки для унитазов": 1122, "Шкафы": 1565, 'Тумбы': 1564}
wh_yandex= {'fbs_ctm': ['ИМOWLT190303', 'ИМSS100'],
            'fbs_express': ['а0026033', 'а0026027', 'а0027471', 'а0027470', 'ИМOWLT190901', 'ИМOWLT200901', 'OWLM200201', 'а0027568', 'ИМMAL80', 'ИМHELLS65', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN60', 'ИМRUNN50', 'ИМRUNN40', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200302', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200100', 'OWLM200101', 'OWLM200102', 'OWLM200301', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLM200202', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190301/2', 'OWLT190303', 'OWLT190303/2', 'OWLT190402', 'OWLT190402/2', 'OWLT190702', 'OWLT190702/2', 'OWLT200901', 'OWLT200901/2', 'OWLT190901', 'OWLT190901/2', 'TOWLT190302', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'OWLT190201'],
            'dbs_our_delivery': ['all']
            }
def check_wh(offer_id):
    if offer_id in wh_yandex['fbs_ctm']:
        result = 'fbs_ctm'
    elif offer_id in wh_yandex['fbs_express']:
        result = 'fbs_ctm'
    else:
        result = 'dbs_our_delivery'

    return result


root = minidom.Document()

date = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(date)
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

deliveryChild = root.createElement('delivery-options')

deliveryOptionChild = root.createElement('option')
deliveryOptionChild.setAttribute('cost', '0')
deliveryOptionChild.setAttribute('days', '3')
deliveryOptionChild.setAttribute('order-before', '13')
deliveryChild.appendChild(deliveryOptionChild)

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

#ЭлементЫ внутри элемента <offer>.??????
#<offer id="belaya-kofta-12345"> sku
#<name>Ударная дрель Makita HP1630, 710 Вт</name>
#<price>3870,50</price>
#<offer id="12345-abcd">
#<description>В комплекте с детским микроскопом есть все.</description>
#<categoryId>743</categoryId>
# <vendor>LEVENHUK</vendor>
# <price>6498</price>
# <count>23</count>
# min-quantity


offersChild = root.createElement('offers')
def create_offer(product_code, count, price):  #(name, vendor, product_code, category_id, description,  url, count, price)

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

    countOfferChild = root.createElement('count')
    textcountOffer = root.createTextNode(count)
    countOfferChild.appendChild(textcountOffer)
    offerChild.appendChild(countOfferChild)

    # minQuantityOfferChild = root.createElement('min-quantity')
    # textMinQuantityOffer = root.createTextNode('4')
    # minQuantityOfferChild.appendChild(textMinQuantityOffer)
    # offerChild.appendChild(minQuantityOfferChild)


need_data = processing_json()
#print(type(need_data), len(need_data))
#
for row in need_data:  #our_data[10:]:
    print(row)
    product_code = row[1]
    price = str(row[2])
    #category_id = str(categories.get(row[1]))
    count = row[3]
    #if count is not None:
    if product_code != '' and count is not None:
        create_offer(product_code, str(count), price)  #(name, vendor, product_code, category_id, description,  url, count, price)
        #print(row)

productChild.appendChild(nameChild)
productChild.appendChild(companyChild)
productChild.appendChild(urlChild)
productChild.appendChild(platformChild)
productChild.appendChild(versionChild)
productChild.appendChild(deliveryChild)
productChild.appendChild(pickupChild)
# productChild.appendChild(currenciesChild)
# currenciesChild.appendChild(currencyChild)

##For add product only? custom:111
#productChild.appendChild(categoriesChild)
productChild.appendChild(offersChild)

xml_root.appendChild(productChild)

xml_str = root.toprettyxml(indent="\t")
#for development
save_path_file = "yandex.xml"
#for production
#save_path_file = "/var/www/html/2c/yandex.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
