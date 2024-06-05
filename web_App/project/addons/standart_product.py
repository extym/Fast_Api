import sys

from sqlalchemy import select

from sqlalchemy.orm import Session
from project import engine
from project.models import Product


def standart_tyres(type_data=None, shop_name=None):
    proxy_data, proxy = [], []
    global_result = {}
    with Session(engine) as session:
        data = session.scalars(select(Product)
                               .where(Product.shop_name == shop_name))\
            .all()
    for row in data:
        prod = row.__dict__
        for key in prod.keys():
            print(key, f"= prod.get('{key}')")

        try:
            opt_price = prod.get('price_product_base')
            date_added = prod.get('date_added')
            set_shop_name = prod.get('set_shop_name')
            description_product_add = prod.get('description_product_add')
            brand_id = prod.get('brand_id')
            final_price = prod.get('final_price')
            date_modifed = prod.get('date_modifed')
            external_sku = prod.get('external_sku')
            uid_edit_user = prod.get('uid_edit_user')
            articul_product = prod.get('articul_product')
            old_price = prod.get('old_price')
            selected_mp = prod.get('selected_mp')
            alias_prod_name = prod.get('alias_prod_name')
            description_category_id = prod.get('description_category_id')
            id = prod.get('id')
            product_id = prod.get('product_id')
            name = prod.get('name_product')
            type_id = prod.get('type_id')
            volume_weight = prod.get('volume_weight')
            shop_name = prod.get('shop_name')
            discount = prod.get('discount')
            status_mp = prod.get('status_mp')
            status_in_shop = prod.get('status_in_shop')
            barcode = prod.get('barcode')
            store_id = prod.get('store_id')
            description = prod.get('description_product')
            images_product = prod.get('images_product')
            shop_k_product = prod.get('shop_k_product')
            cart_id = prod.get('cart_id')
            quantity = prod.get('quantity')
            photo = prod.get('photo')
            price_add_k = prod.get('price_add_k')
            discount_shop_product = prod.get('discount_shop_product')
            vendor = prod.get('brand')
            vendor_code = prod.get('vendor_code')
            reserved = prod.get('reserved')
            id_1c = prod.get('id_1c')
            discount_mp_product = prod.get('discount_mp_product')
            quantity_for_shop = prod.get('quantity_for_shop')
            in_stock = int(quantity) - int(reserved)
            if in_stock >= 4:
                enabled = 1
            else:
                enabled = 0
            if vendor == 'Carwel':
                description = name
            elif vendor == '':
                continue
            category_id = 7000

            if data[i][4] in ['S', 's', 'Летняя']:
                type_tyres = 'Летняя'
            elif data[i][4] in ["W", 'Зимняя']:
                type_tyres = 'Зимняя'
            elif data[i][4] in ["allseason", 'Всесезонная']:
                type_tyres = 'Всесезонная'
            else:
                print('1212_category_id', data[i][4])
            category = 12
            rule = False
            # check category wheels and tyres

            size = data[i][7]  # 16 'diameter'
            width = data[i][8]  # 14
            height = data[i][9]  # 15
            sku = data[i][0]
            name_picture = '88888888'
            image_url = data[i][20]  # image_link
            if image_url:
                # name_picture = 'shins-' + id_generator() + '.png'
                name_picture = 'shins-' + vendor_code + '.png'
            image_tuple = (name_picture, image_url)
            # price = count_price(data[i][17], size)
            koeff = 1
            meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
            meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
            meta_h1 = ' '
            provider = 'shins'
            params = 1
            options = {
                'diameter': size,
                'width': width,
                'profile': height
            }

            global_result.update({vendor.strip() + vendor_code:
                (
                    [category_id, name, description, opt_price,
                     in_stock, enabled, vendor_code, vendor, meta_d, meta_k,
                     params, koeff, meta_h1, provider, category],
                    image_tuple,
                    options,
                    rule
                )})

        except KeyError as error:
            print("Something went wrong KeyError from getcsv: {}".format(error))
            # write(str(data))
            print(str(data[i]))
            continue

    mem = sys.getsizeof(proxy_data)

    print(mem / 1000, 'Kb--')
    print("ALL_RIDE_get_tyres_csv ()".format(len(global_result)))
    return global_result


standart_tyres_csv(shop_name='Low Price')

# def standart_wheels_csv(distributor=None, without_db=False):
#     data = get_data_wheels_csv()
#     global_result = {}
#     for i in range(1, len(data)):
#         if data[i][1] == 'title':
#             continue
#         else:
#             try:
#                 in_stock = int(data[i][17]) + int(data[i][18])
#                 if in_stock >= 4:
#                     enabled = 1
#                 else:
#                     enabled = 0
#                 name = data[i][1]
#                 vendor = data[i][3]
#                 description = name
#                 category_id = categories_wheels.get(vendor)
#                 if category_id is None:
#                     category_id = cats_wheels_upper.get(vendor.upper(), 4000)
#                 category = 5
#                 # check category wheels and tyres
#                 product_code = data[i][2]
#                 diameter = data[i][7].split(' / ')[0]  # 16 'diameter'
#                 width = data[i][7].split(' / ')[1].strip("0").replace('.', ',').strip(',')  # 20
#                 hole = 'D' + data[i][12].strip("0").replace('.', ',')  # 19
#                 bolts_spacing = data[i][8] + '/' + \
#                                 data[i][9].strip("0").replace('.', ',')  # 17
#                 et = 'ET' + data[i][11].strip("0").replace('.', ',').strip(',')  # 18
#                 sku = data[i][0]
#                 name_picture = '777777777'
#                 image_url = data[i][16]  # image_link
#                 if image_url:
#                     name_picture = 'shins-' + product_code + '.png'
#                 image_tuple = (name_picture, image_url)
#                 price_rrc = data[i][15]
#                 price = float(price_rrc)
#                 price_opt = data[i][14]
#                 rule = False
#                 if int(price_opt) * 1.18 >= int(price_rrc):
#                     rule = True
#                 koeff = 1
#                 meta_d = 'летняя и зимняя резина ' + name + ' в интернет-магазине шин и дисков 1000koles.ru'
#                 meta_k = 'летняя и зимняя резина, колеса, цена, купить, в Москве, в интернет-магазине'
#                 meta_h1 = ' '
#                 params = 1
#                 provider = 'shins'
#                 options = {
#                     'et': et,  # 18
#                     "bolts_spacing": bolts_spacing,  # 17
#                     'diameter': diameter,  # 16
#                     'dia': hole,  # 19
#                     'width': width  # 20
#                 }
#                 global_result.update({vendor.strip() + product_code:
#                     (
#                         [category_id, name, description, price, in_stock,
#                          enabled, product_code, vendor, meta_d, meta_k,
#                          params, koeff, meta_h1, provider, category],
#                         image_tuple,
#                         options,
#                         rule,
#                         price_opt
#                     )})
#                 # result = ([category_id, name, description, price, in_stock, enabled, product_code, vendor, meta_d, meta_k,
#                 #            params, koeff, meta_h1, category], image_tuple, options)
#                 # proxy_data.append(result)
#             except Exception as er:
#                 print('fuckup standart getcsv {} {}'.format(er, data[i]))
#
#     if not without_db:
#         check_write_json_v4(global_result)
#         data = standart_tyres_csv()
#         mems = sys.getsizeof(data)
#         print('from_csv', mems / 1000, 'Kb')
#         check_write_json_v4(data)
#
#     print('ALL_RIDE_get_wheels_csv ', len(global_result))
#     return global_result