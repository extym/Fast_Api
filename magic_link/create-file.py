from xml.dom import minidom
import datetime
from prepare_data_export import get_need_data
from connect import check_and_write


desk_carwel = 'Диски CARWEL- cовременный, динамично развивающийся бренд. Новейшее передовое оборудование и современные технологии по производству литых колесных дисков отвечающие самым высоким стандартам качества и надежности,является не единственным конкурентным преимуществом.'
categories = { 'iFree' : 628, 'Carwel' : 1969,  'KHOMEN' : 1968,  'КиК' : 1782 , 'Скад'  : 1926}

check_and_write()

root = minidom.Document()

date = datetime.datetime.now(datetime.timezone.utc).isoformat()
print(date)
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

#currenciesChild = root.createElement('currencies')

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

for key in categories.keys():
    category_vendor = key
    categories_id = categories[category_vendor]
    categoryChild = root.createElement('category')
    categoryChild.setAttribute('id', f'{categories_id}')
    categoryChild.setAttribute('parentId', '1')
    textCategory = root.createTextNode(f'{category_vendor}')
    categoryChild.appendChild(textCategory)
    categoriesChild.appendChild(categoryChild)

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
def create_offer(name, vendor, product_code, category_id, description,  url, count, price):

    offerChild = root.createElement('offer')
    offerChild.setAttribute('id', product_code)
    #offerChild.setAttribute('id', f'162499{y}')
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
    textMinQuantityOffer = root.createTextNode('4')
    minQuantityOfferChild.appendChild(textMinQuantityOffer)
    offerChild.appendChild(minQuantityOfferChild)


need_data = get_need_data()
#print(type(need_data), len(need_data))
for i in range(len(need_data)):  #our_data[10:]:

    name = need_data[i]['name']
    vendor = need_data[i]['vendor']
    product_code = need_data[i]['vendorCode']
    price = need_data[i]['price']['b2b'] * 1.18
    price = str(round(price, 0))
    category_id = str(categories.get(vendor))
    description = need_data[i]['description'][:230]
    if vendor == 'Carwel':
        description = desk_carwel
    count = str(need_data[i]['count'])
    index = need_data[i]['picture'].rfind('/')
    pre_url = need_data[i]['picture'][index + 1:]
    if len(pre_url) < 10:
        pre_url = "11" + pre_url
    url = 'https://www.1000koles.ru/pictures/' + pre_url
    create_offer(name, vendor, product_code, category_id, description,  url, count, price)

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

xml_str = root.toprettyxml(indent="\t")
#for development
# save_path_file = "yandex.xml"
#for production
save_path_file = "/home/ivanovka/data/www/1000koles.ru/pictures/yandex.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
