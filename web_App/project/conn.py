import datetime
import os

import psycopg2
from psycopg2 import OperationalError

from project.creds import db_user, db_host, db_name, db_pass

# from project.conn_maintenance import *


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

create_marketplaces = """
CREATE TABLE IF NOT EXISTS marketplaces (
id SERIAL PRIMARY KEY,
user_id varchar NOT NULL,
seller_id varchar NOT NULL, 
name_mp TEXT NOT NULL,
key_mp varchar NOT NULL,
shop_name TEXT NOT NULL,
shop_id TEXT,
company_id TEXT,
warehouses TEXT,
date_Added varchar,
date_Modifed varchar,
mp_discount float4,
mp_markup float4,
store_discount float4,
store_markup float4,
UNIQUE (id)
)
"""

create_internal_import = """
CREATE TABLE IF NOT EXISTS internal_import (
id SERIAL PRIMARY KEY,
internal_import_mp_1 TEXT NOT NULL,
internal_import_store_1 TEXT NOT NULL,
internal_import_role_1 TEXT NOT NULL,
internal_import_discount_1  int,
internal_import_markup_1  int,
internal_import_mp_2 TEXT NOT NULL,
internal_import_store_2 TEXT NOT NULL,
internal_import_role_2 TEXT NOT NULL,
internal_import_discount_2 int,
internal_import_markup_2  int,
company_id TEXT NOT NULL,
user_id varchar NOT NULL,
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

create_order_items_v2 = """
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    mp_order_id varchar NOT NULL,
    FOREIGN KEY (mp_order_id)
        REFERENCES fresh_orders (id_mp)
        ON UPDATE CASCADE ON DELETE CASCADE,
    shop_order_id varchar,
    shop_name TEXT NOT NULL,
    our_status text,
    article varchar NOT NULL,
    article_mp varchar,
    name TEXT,
    id_1c varchar,
    shop_status TEXT, 
    vendor_code varchar,
    quantity varchar, 
    price varchar,
    add_price TEXT,
    mp TEXT,
    company_id TEXT,
    photo varchar,
    category TEXT,
    shipment_date TEXT,
    order_status TEXT,
    delivery_type TEXT,
    is_cancelled bool,
    date_added varchar,
    date_modifed varchar
    )
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
roles TEXT,
photo text,
date_Added varchar,
date_Modifed varchar,
upload_prices_url text,
upload_price_category varchar,
UNIQUE (email)
)
"""

create_upload_price = """
CREATE TABLE IF NOT EXISTS upload_price (
id SERIAL PRIMARY KEY,
name varchar NOT NULL,
upload_prices_markup int,
upload_price_discount int, 
upload_prices_mp text,
distributors TEXT,
link TEXT,
is_null_stocks text,
is_scheduler text,
date_Added varchar,
date_Modifed varchar,
user_modifed int,
upload_prices_short_shop text,
upload_prices_legal_name text,
upload_prices_store text,
upload_option varchar,
upload_prices_url text,
upload_price_category text,
user_id int,
UNIQUE (id)
)
"""

create_distributors = """
CREATE TABLE IF NOT EXISTS distributors (
id SERIAL PRIMARY KEY,
name varchar NOT NULL,
koef_price int,
distributor TEXT,
login_api_dist text,
key_api_dist text,
api_link text,
type_downloads varchar,
link_downloads text,
is_scheduler bool,
date_Added varchar,
date_Modifed varchar,
user_modifed int,
UNIQUE (id)
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
store_id TEXT,
quantity INT,
reserved INT,
price_product_base int,
price TEXT,
old_price TEXT,
discount float4,
description_product TEXT,
photo varchar,
date_Added varchar,
date_Modifed varchar,
id_1c varchar,
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
shop_k_product float4,
discount_shop_product float4,
quantity_for_shop INT,
description_product_add text,
uid_edit_user INT,
final_price float4,
barcode TEXT, 
vendor_code text,
UNIQUE (articul_product, store_id)
)
"""

create_attributes_product = """
CREATE TABLE IF NOT EXISTS  attributes_product (
    id SERIAL PRIMARY KEY,
    articul_product varchar,
    FOREIGN KEY (id)
        REFERENCES products (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    depth varchar,
    width varchar,
    height varchar,
    dimension_unit varchar,
    weight varchar,
    weight_unit varchar,
    name_category_id varchar,
    category_mark varchar,
    category_sign varchar,
    mark_1 varchar,
    mark_2 varchar,
    mark_3 varchar,
    mark_4 varchar,
    mark_5 varchar,
    vat varchar,
    visible bool,
    commissions varchar,
    is_prepayment bool,
    is_prepayment_allowed bool,
    is_kgt bool,
    discounted_stocks varchar,
    sku int,
    type_id int,
    volume_weight float4, 
    UNIQUE (id)
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

create_products_old = """
CREATE TABLE IF NOT EXISTS products (
id SERIAL PRIMARY KEY,
articul_product varchar NOT NULL,
shop_name varchar, 
store_id TEXT,
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
shop_k_product float4,
discount_shop_product float4,
quantity_for_shop INT,
description_product_add text,
uid_edit_user INT,
final_price float4,
UNIQUE (articul_product, store_id)
)
"""

create_attribute_product_old = """
CREATE TABLE IF NOT EXISTS  attributes_product (
    id SERIAL PRIMARY KEY,
    articul_product varchar,
    FOREIGN KEY (articul_product)
        REFERENCES products (articul_product, store_id)
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

create_products_2 = """
CREATE TABLE IF NOT EXISTS products (
id SERIAL PRIMARY KEY,
articul_product varchar NOT NULL,
shop_name varchar, 
store_id TEXT,
quantity INT,
reserved INT,
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
shop_k_product float4,
discount_shop_product float4,
quantity_for_shop INT,
description_product_add text,
uid_edit_user INT,
final_price float4,
attributes_product INT,
UNIQUE (articul_product, store_id)
)
"""

create_attributes_product_2 = """
CREATE TABLE IF NOT EXISTS  attributes_product (
    id SERIAL PRIMARY KEY not null ,
    prod_id INT,
    articul_product varchar,
    depth varchar,
    width varchar,
    height varchar,
    dimension_unit varchar,
    weight varchar,
    weight_unit varchar,
    barcode varchar,
    category_id_oson varchar,
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
    type_id int,
    volume_weight float4, 
    UNIQUE (id)
    )
"""

# custom_create_all = [create_fresh_orders_table,
#                      create_marketplaces,
#                      create_order_items,
#                      create_users,
#                      create_products,
#                      create_attribute_product,
#                      create_sales
#                      ]


query_read_order = (" SELECT * from fresh_orders "
                    " WHERE id_mp = %s and shop_name = %s ")

query_write_order = ("INSERT INTO fresh_orders "
                     "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
                     "shipment_Date, status, our_status, payment_Type, delivery)"
                     "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

query_write_order_2 = ("INSERT INTO fresh_orders "
                       "(id_mp, our_id, date_Added, date_Modifed, shop_Name, mp, "
                       "shipment_Date, status, our_status, payment_Type, delivery)"
                       "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s, %s)")

query_write_items = ("INSERT INTO order_items "
                     "(id_mp, shop_order_id, shop_Name, "
                     "our_status, vendor_code, id_1c, quantity, price, "
                     "date_Added, date_Modifed)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

query_write_items_v2 = ("INSERT INTO order_items "
                        "(mp_order_id, shop_order_id, mp, shop_Name, order_status, "
                        "our_status, vendor_code, id_1c, quantity, price, article, article_mp, "
                        "date_Added, date_Modifed)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())")

query_rm_full_order = (" SELECT * from fresh_orders, order_items "
                       " WHERE id_mp = %s")

query_read_items = (" SELECT * from order_items "
                    " WHERE id_ip = %s and shop_name = %s ")

read_new_order = (" SELECT * from fresh_orders "
                  " WHERE our_status = 'NEW' ")

read_order_items = (" SELECT * from order_items "
                    " WHERE id_mp = %s and shop_name = %s ")

update_send_data_order = (
    " UPDATE fresh_orders SET dateSendData = NOW(), dateModifed = NOW(), ourStatus = 'SEND_TO_1C' "
    " WHERE id_MP = %s and shop_name = %s ")

update_status_order = (" UPDATE fresh_orders "
                       "SET status = %s, our_status = %s, "
                       " date_modifed = NOW() "
                       "WHERE id_MP = %s and shop_name = %s ")

update_status_order_items = (" UPDATE order_items "
                             "SET order_status = %s, our_status = %s,"
                             " date_modifed = NOW() "
                             "WHERE mp_order_id = %s and shop_name = %s ")

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


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=5432
        )
        # print("Connection to DB successfully")

    except OperationalError as error:
        print(f'The ERROR "{error}" occurred')

    return connection


def get_distibutor_link(distibutor, type_downloads, name):
    query = " SELECT link_downloads " \
            " FROM distributors" \
            " WHERE distributor = %s and type_downloads = %s and name = %s "
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, [distibutor, type_downloads, name])
            raw_data = cursor.fetchall()
            # print("Query from execute_query executed successfully")
    return raw_data



async def execute_query(query, data):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        print("Query from execute_query executed successfully")

    except OperationalError as err:
        print(f"The ERROR from execute_query '{err}' occured ")

    cursor.close()
    connection.close()


async def execute_query_v4(query=None, query2=None, data=None):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if query:
            cursor.execute(query, data)
        if query2:
            cursor.execute(query2, data)
            # print("Query from execute_query_v2 executed successfully")

    except OperationalError as err:
        print(f"The ERROR from execute_query '{err}' occured ")

    cursor.close()
    connection.close()


async def execute_query_v2(query, data):
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                print("Query from execute_query executed successfully")

    except (OperationalError, psycopg2.DatabaseError) as err:
        print(f"The ERROR from execute_query '{err}' occured ")


def execute_query_v3(query, data):
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, data)
                print("Query from execute_query executed successfully")

    except (OperationalError, psycopg2.DatabaseError) as err:
        print(f"The ERROR from execute_query '{err}' occured ")


async def executemany_query(query, data):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        print("Query from execute_many_query executed successfully")

    except OperationalError as err:
        print(f"The ERROR from execute_many_query '{err}' occured ")

    cursor.close()
    connection.close()


async def executemany_query_v2(query, data):
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                print("Query from execute_many_query executed successfully")

    except (OperationalError, psycopg2.DatabaseError) as err:
        print(f"The ERROR from execute_many_query '{err}' occured ")


def executemany_query_v3(query, data):
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                print("Query from execute_many_query executed successfully")

    except (OperationalError, psycopg2.DatabaseError) as err:
        print(f"The ERROR from execute_many_query '{err}' occured ")


async def write_order(query1: str = None, data1: object = None,
                      query2: str = None, data2: object = None) -> object:
    with create_connection() as connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query1, data1)
                # print("Query write_order executed successfully")
        except OperationalError as err:
            print(f"The ERROR write_order '{err}' occured ")

        try:
            with connection.cursor() as cursor:
                cursor.executemany(query2, data2)
                # print("Query write_order_items executed successfully")
        except OperationalError as err:
            print(f"The ERROR write_order_items '{err}' occured ")


def execute_query_return_id(connection, query, data):
    connection.autocommit = True
    cursor = connection.cursor()
    lastrowid = None
    try:
        cursor.execute(query, data)
        lastrowid = cursor.lastroid()
        print("Query from execute_query_return_id executed successfully")

    except OperationalError as err:
        print(f"The ERROR from execute_query_return_id '{err}' occured ")

    cursor.close()

    return lastrowid


def check_order(query, data):
    connection = create_connection()
    cursor = connection.cursor()
    re_data = None
    try:
        cursor.execute(query, data)
        re_data = cursor.fetchall()
        print("Query from check_order executed successfully")
    except OperationalError as err:
        print(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return re_data


def check_is_exist(query, data):
    connection = create_connection()
    cursor = connection.cursor()
    result = False
    try:
        cursor.execute(query, data)
        redata = cursor.fetchone()
        print(f"Query from check_is_exist '{data[0]}' executed successfully")
        if redata is not None:
            result = True
    except OperationalError as err:
        print(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return result


# check_order( query_read_order, ("MP2713064-001", 'Leroy'))


def get_one_order():
    connection = create_connection()
    result, proxy = None, []
    try:
        cursor = connection.cursor()
        cursor.execute(read_new_order)
        result = cursor.fetchone()
        print("Fetching single row", result)
        if result is not None:
            data = (result[1], result[7])
            print("Fetching single row-------", data)
            cursor.execute(read_order_items, data)
            items = cursor.fetchall()
            proxy = [item for item in items]

        cursor.close()

    except psycopg2.Error as error:
        print("Failed to read data from table", error)
    finally:
        if connection:
            connection.close()
            print("The Sql connection is closed")

    return result, proxy


# connection = create_connection()
# create_database_query = "CREATE DATABASE stm_app"
# create_database(connection, create_database_query)

def maintenans_query(query):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query from maintenans_query executed successfully")

    except OperationalError as err:
        print(f"The ERROR from maintenans_query '{err}' occured ")

    cursor.close()
    connection.close()


query_join = "select * from fresh_orders join order_items oi on fresh_orders.id_mp = oi.mp_order_id where " \
             "fresh_orders.date_added<'%2024-05-29'"
query_insert = "insert  INTO sales ( mp_order_id, shop_order_id, date_added, shop_name, mp, shipment_date, " \
               "order_status, shop_status, delivery_type, article, id_1c, quantity,  price, date_added, date_modifed )" \
               "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now() )"


def rewrite_orders(query1, query2):
    try:
        connection = create_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        # cursor.close()

        # re_data_row = (id_mp, shop_id, date_added, mp_name, shipment_date, status, our_status, delivery_type, price)
        re_data = [(i[0], i[2], i[2], i[7], i[8], i[9], i[10], i[16], i[24]) for i in data]

        # re_data_row = (id_mp, shop_id, date_added, mp_name, shipment_date, status, our_status, delivery_type,
        # vendor_code, id_ic, quantity, price)
        all_data = [(i[0], i[1], i[2], i[7], i[8], i[9], i[10], i[16], i[21], i[22], i[23], i[24]) for i in data]

        cursor.executemany(query2, all_data)

        print(len(data[0]), data[0])
        return True
    except:
        return False


def rewrite_orders_v2(query1, query2):
    try:
        connection = create_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query1)
        data = cursor.fetchall()
        # cursor.close()

        # re_data_row = (id_mp, shop_id, date_added, mp_name, shipment_date, status, our_status, delivery_type, price)
        re_data = [(i[0], i[2], i[2], i[7], i[8], i[9], i[10], i[16], i[24]) for i in data]

        # re_data_row = (id_mp, shop_id, date_added, mp_name, shipment_date, status, our_status, delivery_type,
        # vendor_code, id_ic, quantity, price)
        all_data = [(i[0], i[1], i[2], i[2], i[7], i[8], i[9], i[10], i[16], i[21], i[22], i[23], i[24]) for i in data]

        cursor.executemany(query2, all_data)

        print(len(data[0]), data[0])
        os.abort()
        return True
    except:
        return False


def rewrite_orders_v3():
    HOUR = '09:00:00'
    example = datetime.datetime.today().strftime(f"%Y-%m-%d {HOUR}")
    need_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime(f"%Y-%m-%d {HOUR}")
    # print(example, example > need_date)
    # print(need_date, example > need_date)
    # if example < need_date:  # it's current time more 09 AM
    query_join_v2 = "select * from fresh_orders join order_items oi on fresh_orders.id_mp = oi.mp_order_id where " \
                    f"fresh_orders.date_added< '{need_date}'"
    # print(333, need_date, type(need_date))

    try:
        connection = create_connection()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(query_join_v2)
        data = cursor.fetchall()

        # re_data_row = (
        # id_mp, shop_id, date_added, mp_name, shipment_date,
        # status, our_status, delivery_type, price)
        # re_data = [(i[0], i[2], i[2], i[7], i[8],
        #             i[9], i[10], i[16], i[24]) for i in data]
        # print(11, re_data)
        # re_data_row = (
        # id_mp, shop_id, date_added, mp_name, shipment_date, status,
        # our_status, delivery_type,
        # vendor_code, id_ic, quantity, price)
        all_data = [(i[0], i[1], i[2], i[2], i[7], i[8],
                     i[9], i[10], i[16], i[21], i[22],
                     i[23], i[24]) for i in data]

        # cursor.executemany(query_insert, all_data)

        print(11, len(data), data[0])
        print(22, len(all_data), all_data[0])
        cursor.close()
        return True
    except:
        return False


custom_create_all = [create_fresh_orders_table,
                     create_marketplaces,
                     create_order_items_v2,
                     create_users,
                     create_products,
                     create_attributes_product,
                     create_sales,
                     create_internal_import
                     ]

upgrade_db = [create_marketplaces,
              create_users,
              create_products,
              create_attributes_product,
              create_sales,
              create_internal_import
              ]

update_db = [
    # "alter table public.products alter column price_product_base type int using price_product_base::int",
    # "alter table public.marketplaces alter column key_mp type varchar(1000) using key_mp::varchar(1000)",
    # "alter table order_items rename column our_order_id to shop_order_id",
    "alter table order_items rename column id_mp to mp_order_id",
    "alter table order_items add column article varchar",
    "alter table order_items add column article_mp varchar",
    "alter table order_items add column name varchar",
    "alter table order_items add column mp varchar",
    "alter table order_items add column company_id varchar",
    "alter table order_items add column add_price text",
    "alter table order_items add column photo varchar",
    "alter table order_items add column category text",
    "alter table order_items add column shipment_date text",
    "alter table order_items add column order_status text",
    "alter table order_items add column shop_status text",
    "alter table order_items add column delivery_type varchar",
    "alter table order_items add column delivery_point varchar",
    "alter table order_items add column is_cancelled bool",
    "alter table order_items add column date_added varchar",
    "alter table order_items add column date_modifed varchar",
    "alter table public.order_items add id integer",
]

# for query in custom_create_all:
#     maintenans_query(query)

# for query in update_db:
#     maintenans_query(query)

# print(rewrite_orders_v3())
# print(rewrite_orders_v2(query_join, query_insert))
# # rewrite_orders("select * from fresh_orders  where date_added<'%2023-03-29'")

# maintenans_query(create_fresh_orders_table)
# maintenans_query(create_order_items)
# maintenans_query(create_users)
# maintenans_query(create_marketplaces)
# maintenans_query(create_users)
# maintenans_query(create_consult_users)

#
# maintenans_query(create_products)
# maintenans_query(create_attributes_product)
# # maintenans_query(create_sales)
# maintenans_query(create_attributes_product)
# maintenans_query(create_internal_import)
# maintenans_query(create_upload_price)
maintenans_query(create_attributes_product)

