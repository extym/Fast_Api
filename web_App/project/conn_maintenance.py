create_fresh_orders_table = """
CREATE TABLE IF NOT EXISTS fresh_orders (
id SERIAL PRIMARY KEY,
id_mp varchar NOT NULL,
our_id varchar,
date_Added varchar,
date_Modifed varchar,
date_Send_Data varchar,
date_1c varchar,
shop_name TEXT,
mp text,
shipment_Date varchar,
status TEXT,
our_status TEXT, 
is_cancelled TEXT,
mp_feachers varchar,
payment_Type TEXT,
summ_Order varchar,
bussines_Id TEXT,
delivery varchar, 
UNIQUE (id_mp)
)
"""

create_market_cred = """
CREATE TABLE IF NOT EXISTS marketplaces (
id SERIAL PRIMARY KEY,
user_id varchar NOT NULL,
seller_id varchar NOT NULL, 
name_mp TEXT NOT NULL,
key_mp varchar NOT NULL,
shop_name TEXT NOT NULL,
company_id TEXT,
warehouses TEXT,
date_Added varchar,
date_Modifed varchar,
UNIQUE (id)
)
"""

create_delivered_orders_table = """
CREATE TABLE IF NOT EXISTS send_orders (
id SERIAL PRIMARY KEY,
id_mp varchar NOT NULL,
our_Id varchar,
date_Added varchar,
date_Modifed varchar,
date_SendData varchar,
shop_name TEXT NOT NULL,
shipment_Date varchar,
status TEXT NOT NULL,
mp_feachers varchar,
payment_Type TEXT,
bussines_Id TEXT,
delivery varchar
)
"""

create_order_items = """
CREATE TABLE IF NOT EXISTS order_items (
    id_mp varchar NOT NULL,
    FOREIGN KEY (id_mp)
        REFERENCES fresh_orders (id_mp)
        ON UPDATE CASCADE ON DELETE CASCADE,
    our_order_id varchar,
    shop_name TEXT NOT NULL,
    our_status TEXT NOT NULL, 
    vendor_code varchar NOT NULL,
    id_1c varchar NOT NULL,
    quantity varchar NOT NULL, 
    price varchar)
"""


create_send_order_items = """
CREATE TABLE IF NOT EXISTS send_order_items (
    id_mp varchar NOT NULL,
    FOREIGN KEY (id_mp)
        REFERENCES send_orders (id_mp)
        ON UPDATE CASCADE ON DELETE CASCADE,
    our_order_id varchar,
    shop_name TEXT NOT NULL,
    our_status TEXT NOT NULL, 
    vendor_code varchar NOT NULL,
    id_1c varchar NOT NULL,
    quantity varchar NOT NULL, 
    price varchar)
"""


create_users = """
CREATE TABLE IF NOT EXISTS users (
id SERIAL PRIMARY KEY,
email varchar NOT NULL,
password varchar NOT NULL, 
name TEXT NOT NULL,
company_id TEXT,
role TEXT,
date_Added varchar,
date_Modifed varchar,
UNIQUE (email)
)
"""

create_consult_users = """
CREATE TABLE IF NOT EXISTS consult_users (
id SERIAL PRIMARY KEY,
email varchar NOT NULL,
current_user_id varchar NOT NULL, 
phone TEXT NOT NULL,
name TEXT,
role TEXT,
company_id TEXT,
date_Added varchar,
date_Modifed varchar,
UNIQUE (id)
)
"""


create_products = """
CREATE TABLE IF NOT EXISTS products (
id SERIAL PRIMARY KEY,
articul_product varchar NOT NULL,
shop_name varchar, 
company_id TEXT,
quantity INT,
price TEXT,
discount float4,
description_product TEXT,
photo varchar,
date_Added varchar,
date_Modifed varchar,
id_1c varchar,
price_product_base float4,
selected_mp TEXT,
name_product TEXT,
status_mp TEXT,
images_product TEXT,
price_add_k float4,
discount_mp_product float4,
set_shop_name TEXT,
external_sku varchar,
alias_prod_name varchar,
status_in_shop TEXT,
photo_line varchar,
shop_k_product float4,
discount_shop_product float4,
quantity_for_shop INT,
description_product_add text,
uid_edit_user INT,
final_price float4,
UNIQUE (articul_product)
)
"""


create_attribute_product = """
CREATE TABLE IF NOT EXISTS  attributes_product (
    id SERIAL PRIMARY KEY,
    articul_product varchar,
    FOREIGN KEY (articul_product)
        REFERENCES products (articul_product)
        ON UPDATE CASCADE ON DELETE CASCADE,
    depth varchar,
    width varchar,
    height varchar,
    dimension_unit varchar,
    weight varchar,
    weight_unit varchar,
    barcode varchar,
    category_id varchar,
    created_at varchar,
    images varchar,
    marketing_price varchar,
    min_ozon_price varchar,
    old_price varchar,
    premium_price varchar,
    price varchar,
    recommended_price varchar,
    min_price varchar,
    stocks int,
    vat varchar,
    visible bool,
    commissions varchar,
    is_prepayment bool,
    is_prepayment_allowed bool,
    images360 varchar,
    color_image varchar,
    primary_image varchar,
    is_kgt bool,
    discounted_stocks varchar,
    sku int,
    description_category_id int,
    type_id int
    )
"""

create_sales = """
CREATE TABLE IF NOT EXISTS sales (
id SERIAL PRIMARY KEY,
shop_order_id varchar,
mp_order_id varchar,
article varchar NOT NULL,
article_mp varchar,
id_1c varchar,
name TEXT,
shop_name varchar, 
mp text NOT NULL,
company_id TEXT,
quantity INT,
price TEXT,
add_price TEXT,
discount float4,
description TEXT,
photo varchar,
category TEXT,
shipment_date TEXT,
delivery_type varchar,
delivery_point varchar,
order_status varchar,
shop_status varchar,
returned bool,
date_Added varchar,
date_Modifed varchar,
UNIQUE (id)
)
"""

query_read_order = (" SELECT * from fresh_orders "
                         " WHERE id_mp = %s and shop_name = %s ")


query_write_order = ("INSERT INTO fresh_orders "
    "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
                     "shipment_Date, status, our_status, payment_Type, delivery)"
                     "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")


query_write_items = ("INSERT INTO order_items "
    "(id_mp, our_order_id, shop_Name, "
                     "our_status, vendor_code, id_1c, quantity, price)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

# query_write_order_items = ("INSERT INTO order_items "
#     "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
#                      "shipment_Date, status, our_status, payment_Type, delivery)"
#                      "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

query_rm_full_order = (" SELECT * from fresh_orders, order_items "
                         " WHERE id_mp = %s")


query_read_items = (" SELECT * from order_items "
                    " WHERE id_ip = %s and shop_name = %s ")

read_new_order = (" SELECT * from fresh_orders "
                    " WHERE our_status = 'NEW' ")

read_order_items = (" SELECT * from order_items "
                    " WHERE id_mp = %s and shop_name = %s ")


update_send_data_order = (" UPDATE fresh_orders SET dateSendData = NOW(), dateModifed = NOW(), ourStatus = 'SEND_TO_1C' "
                          " WHERE id_MP = %s and shop_name = %s ")


update_status_order = (" UPDATE fresh_orders "
                       "SET status = %s, our_status = %s "
                       "WHERE id_MP = %s and shop_name = %s ")


update_status_order_reverse_id = (" UPDATE fresh_orders "
                       "SET status = %s, our_status = %s "
                       "WHERE our_id = %s and shop_name = %s ")


rewrite_status_order = (" UPDATE fresh_orders "
                       "SET status = %s "
                       "WHERE id_MP = %s and shop_name = %s ")

rebase_order = (" UPDATE fresh_orders "
               "SET our_status = %s "
               "WHERE id = %s and id_MP = %s ")


strong_rebase_order = (" INSERT INTO send_orders "
    "(id_mp, our_order_id, shop_Name, our_status, vendor_code, id_1c, quantity, price)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")


