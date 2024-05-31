import asyncio
import json
import logging
import os

import psycopg2
from psycopg2 import OperationalError
# from conn_maintenance import *
from cred import *


create_fresh_orders = """
CREATE TABLE IF NOT EXISTS fresh_orders (
id SERIAL PRIMARY KEY,
order_id_mp varchar NOT NULL,
our_order_id varchar,
date_Added varchar,
date_Modifed varchar,
date_Send_Data varchar,
data_1c varchar,
mp_name text,
target_link text,
client_id_ps text,
shipment_date varchar,
order_create_date varchar,
status TEXT,
substatus text, 
our_status TEXT, 
is_cancelled bool,
mp_feachers varchar,
payment_Type TEXT,
summ_Order varchar,
bussines_Id TEXT,
delivery varchar, 
UNIQUE (order_id_mp)
)
"""

create_order_items = """
CREATE TABLE IF NOT EXISTS order_items (
    id serial PRIMARY KEY,
    order_id_mp varchar NOT NULL,
    FOREIGN KEY (order_id_mp)
        REFERENCES fresh_orders (order_id_mp)
        ON UPDATE CASCADE ON DELETE CASCADE,
    our_order_id varchar,
    mp_name text,
    store_name text,
    offer_id text,
    our_status text, 
    vendor_code text, 
    vendor text,
    id_1C varchar,
    quantity int,
    price text
)
"""



create_stores = """
CREATE TABLE IF NOT EXISTS stores (
id SERIAL PRIMARY KEY,
client_id varchar,
key_store varchar, 
compain_id TEXT,
date_Added varchar,
date_Modifed varchar,
user_id int,
api_key_ps TEXT,
upload_link TEXT,
mp_name TEXT,
model text,
UNIQUE (client_id)
)
"""


create_customers = """
CREATE TABLE IF NOT EXISTS customers (
    id serial PRIMARY KEY,
    order_id_mp varchar NOT NULL,
    FOREIGN KEY (order_id_mp)
        REFERENCES fresh_orders (order_id_mp)
        ON UPDATE CASCADE,
    our_order_id varchar,
    mp_name text,
    store_name text,
    our_status text, 
    summ_order int,
    phone text,
    email text,
    fias_regionId varchar,
    fias_destinationId varchar,
    geo_lat varchar,
    geo_lon varchar,
    regionKladrId varchar,
    regionWithType varchar,
    cityWithType varchar,
    order_create_date varchar
)
"""


create_fresh_bids = """
CREATE TABLE IF NOT EXISTS fresh_bids (
id SERIAL PRIMARY KEY,
chat_id varchar NOT NULL,
our_id varchar,
date_Added varchar,
date_Modifed varchar,
date_Send_Data varchar,
user_id int,
price text,
target_link text,
msg_id text,
title text,
first_answer bool,
rewrite_leads bool,
leads_id int,
contact_id int,
status TEXT,
our_status TEXT, 
is_cancelled TEXT,
mp_feachers varchar,
payment_Type TEXT,
summ_Order varchar,
bussines_Id TEXT,
delivery varchar, 
UNIQUE (chat_id)
)
"""


logging.basicConfig(filename=LOG_DIR + '/webhook.log', level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")




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


def execute_query_v2(query, data):
    with create_connection() as connection:
        connection.autocommit = True
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                # print("Query from execute_query executed successfully")
                return True
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")
                return False

async def execute_query(query, data):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    # try:
    cursor.execute(query, [data])
        # print("Query from execute_query executed successfully")

    # except OperationalError as err:
    #     print(f"The ERROR from execute_query '{err}' occured ")

    cursor.close()
    connection.close()





async def execute_query_v3(query, data):
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, data)
                # print("Query from execute_query executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")


def execute_query_return_v3(query, data):
    raw_data = []
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, [data])
                raw_data = cursor.fetchall()
                # print("Query from execute_query executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")

    return raw_data


def execute_query_return_one(query, data):
    raw_data = None
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, [data])
                raw_data = cursor.fetchone()
                # print("Query from execute_query executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")

    return raw_data


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
        logging.info('check_order', query, data)
        cursor.execute(query, data)
        re_data = cursor.fetchall()
        logging.info("Query from check_order executed successfully")
    except OperationalError as err:
        logging.error(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return re_data


def get_bid(chat_id=None, leads_id=None):
    bid = []
    with create_connection() as connection:
        with connection.cursor() as cursor:
            if chat_id:
                cursor.execute(query_get_bid_for_chat_id, (chat_id, ))
                row_data = cursor.fetchone()
            elif leads_id:
                cursor.execute(query_get_bid_for_lead_id, (leads_id, ))
                row_data = cursor.fetchone()
            if row_data:
                #############
                # {chat_id: (
                # price, # [7]
                # target_link, # [8]
                # msg_id, # [9]
                # user_id, # [6]
                # title, # [10]
                # first_answer,  # [11]
                # rewrite_leads,  # [12]
                # leads_id, # [13]
                # contact_id)}  # [14]
                bid = (
                    row_data[7],
                    row_data[8],
                    row_data[9],
                    row_data[6],
                    row_data[10],
                    row_data[11],
                    row_data[12],
                    row_data[13],
                    row_data[14]
                )
    logging.info('We_try_get_bid {} {}'.format(chat_id, bid))
    return bid


def check_is_exist_in_db(query, data):
    connection = create_connection()
    cursor = connection.cursor()
    result = False
    try:
        cursor.execute(query, data)
        redata = cursor.fetchone()
        logging.info(f"Query from check_is_exist_in_db '{data[0]}' executed successfully")
        if redata is not None:
            result = True
    except OperationalError as err:
        logging.info(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return result


def check_is_exist_message_in_db_v2(msg_id, chat_id):
    compare = False
    first_answer = False
    rewrite_lead = False
    # redata = (result, 0, 0)
    with create_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query_check_is_message_exist, (chat_id,))
                redata = cursor.fetchone()

                if redata is not None and redata[0] == msg_id:
                    compare = True
                if redata is not None:
                    first_answer = redata[1]
                    rewrite_lead = redata[2]
                    logging.info(f"Query from check_is_exist_in_db '{msg_id, chat_id, redata}' executed successfully")
                    return compare, first_answer, rewrite_lead

            except OperationalError as err:
                logging.info(f"The ERROR from check_order '{err}' occured ")

    return compare, first_answer, rewrite_lead


# check_order( query_read_order, ("MP2713064-001", 'Leroy'))


def check_order_exist(query, data):
    result = False
    status = None
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, [data])
                raw_data = cursor.fetchone()
                if raw_data is not None:
                    result = True
                    status = raw_data[10]
                # print(f"Query from execute_query {raw_data, status} executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")

    return result, status



def execute_query_return_bool(query, data):
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, data)
                return True
                # print("Query from execute_query executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")
                return False


def executemany_return_bool(query, data):
    with create_connection() as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.executemany(query, data)
                return True
                # print("Query from execute_query executed successfully")
            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")
                return False

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


query_write_bid = ("INSERT INTO fresh_bids "
                   "(chat_id, date_added, date_modifed, "
                   " price, target_link, msg_id, user_id, "
                   "title, first_answer, rewrite_leads,"
                   "leads_id, contact_id)"
                   "VALUES (%s, NOW(), now(), %s, %s, %s, %s, %s, %s, %s, %s, %s )")

query_update_msg_id = ("UPDATE fresh_bids SET msg_id = %s, date_modifed = NOW() "
                       "WHERE chat_id = %s ")

query_update_contact_id = ("UPDATE fresh_bids SET leads_id = %s, "
                           "contact_id = %s, date_modifed = NOW() "
                           "WHERE chat_id = %s ")

query_check_is_message_exist = \
    "SELECT msg_id, first_answer, rewrite_leads " \
    "FROM fresh_bids WHERE chat_id=%s "

query_get_bid_for_chat_id = \
    "SELECT * FROM fresh_bids WHERE chat_id = %s"

query_get_bid_for_lead_id = \
    "SELECT * FROM fresh_bids WHERE leads_id = %s"

query_get_all_shops = \
    "SELECT * FROM stores WHERE mp_name= %s"

query_is_exist_order = \
    "SELECT * FROM fresh_orders WHERE order_id_mp = %s"

query_write_order = \
    "INSERT INTO  fresh_orders ( order_id_mp, mp_name, " \
    "shipment_date, order_create_date, date_added, status, " \
    "substatus, our_status, payment_type, delivery, " \
    "summ_order, client_id_ps )" \
    "VALUES (%s, %s, %s, %s, now(), %s, %s, %s, %s, %s, %s, %s)"

query_write_items = \
    " INSERT INTO order_items ( order_id_mp, mp_name, offer_id, " \
                    " id_1c, quantity, price ) " \
                    " VALUES ( %s, %s, %s, %s,  %s, %s )"

query_write_customer =\
    " INSERT INTO customers ( order_id_mp, mp_name, order_create_date, " \
   " summ_order, phone, email, fias_regionId, fias_destinationId,  " \
   " geo_lat, geo_lon, regionKladrId, regionWithType, cityWithType) " \
   " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"

update_order_and_items = \
    " UPDATE fresh_orders SET status = %s " \
                         " WHERE order_id_mp = %s "

query_add_settings_ym = \
    (" INSERT INTO stores "
     "(client_id, key_store, campain_id, api_key_ps, upload_link) "
     "VALUES ( %s, %s, %s, %s, %s )")

query_add_settings_without_ym = \
    (" INSERT INTO stores "
     "(client_id, key_store, campain_id, api_key_ps, upload_link) "
     "VALUES ( %s, %s, %s, %s, %s )")

proxy = ("u2i-TOYzRVLyb9Hw_l7u2aBTVg", '4391',
         "https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/trw_df4110_torm.disk_per.vent.280x24_4_otv_3364311913",
         'e737d71dcddc238d5a1db962f3fb6db9', 353207078, "TRW DF4110 Торм.диск пер.вент.280x24 4 отв",
         True, False, 0, 0)

query_get_shop_client_id = \
    (" SELECT  FROM stores WHERE campain_id = %s")


query_get_shop_campain_id = \
    (" SELECT model, client_id FROM stores WHERE campain_id = %s")

def rewrite_bid_from_json(file):
    with open(file) as f:
        data = json.load(f)
        count, errors = 0, 0
        for key, value in data.items():
            proxy = list(value)
            proxy.insert(0, key)
            try:
                execute_query_v2(query_write_bid, tuple(proxy))
                count += 1
                print(count)
            except:
                errors += 1
                print("errors {}".format(errors))
                continue


def rewrite_bid_from_2_json(file, file2):
    data = dict()
    count, errors = 0, 0
    with open(file) as f:
        data1 = json.load(f)
        data.update(data1)
    with open(file2) as ff:
        data2 = json.load(ff)
        data.update(data2)

    for key, value in data.items():
            proxy = list(value)
            proxy.insert(0, key)
            try:
                execute_query_v2(query_write_bid, tuple(proxy))
                count += 1
                print(count)
            except:
                errors += 1
                print("errors {}".format(errors))
                continue



# maintenans_query(create_fresh_bids)
# maintenans_query(create_fresh_orders)
# maintenans_query(create_order_items)
# maintenans_query(create_stores)

# maintenans_query(create_customers)

# execute_query_v2(query_write_bid, proxy)
# print(get_bid("u2i-TOYzRVLyb9Hw_l7u2aBTVg"))
# print(check_is_exist_in_db(query_check_is_message_exist, ("u2i-TOYzRVLyb9Hw_l7u2aBTVg",)))
# print(check_is_exist_message_in_db_v2('e737d71dcddc238d5a1db962f3fb6db9', "u2i-TOYzRVLyb9Hw_l7u2aBTVg"))
# asyncio.run(execute_query_v3(query_update_msg_id, ('962f3fb6db9', "u2i-TOYzRVLyb9Hw_l7u2aBTVg")))

# rewrite_bid_from_2_json('links.json', 'links.json.old')

# asyncio.run(executemany_query(query_write_items, [('6111114952', 'Sber',  'BV001950-k', '', 1, '990'), ('6111114952',  'Sber',  'delivery', '', 1, '200')]))

# asyncio.run(execute_query_v3(query_write_customer, ('61111152', 'Sber', '2022-11-12', '1190', '88888888888', 'test@test.com', '0c5b2444-70a0-4932-980c-b4dc0d3f02b5', '4cbce9f3-6fd7-4162-962d-41268b75aadc', '55.751812', '37.599292', '77', 'г Москва', 'г Москва')))