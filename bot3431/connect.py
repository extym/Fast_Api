import psycopg2
from psycopg2 import OperationalError
# from conn_maintenance import *
from cred import *

create_order_items = """
CREATE TABLE IF NOT EXISTS order_items (
    id PRIMARY KEY,
    chat_id varchar NOT NULL,
    FOREIGN KEY (chat_id)
        REFERENCES fresh_bids (id)   ### id - ??????  
        ON UPDATE CASCADE ON DELETE CASCADE,
    our_order_id varchar,
    shop_name TEXT NOT NULL,
    our_status TEXT NOT NULL, 
    vendor_code varchar NOT NULL,
    id_1c varchar NOT NULL,
    quantity varchar NOT NULL, 
    price varchar)
"""

create_customers = """
CREATE TABLE IF NOT EXISTS customers (
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
        print("Connection to DB successfully")

    except OperationalError as error:
        print(f'The ERROR "{error}" occurred')

    return connection


def execute_query_v2(query, data):
    with create_connection() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute(query, data)
                print("Query from execute_query executed successfully")

            except OperationalError as err:
                print(f"The ERROR from execute_query '{err}' occured ")


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


async def execute_query_v3(query, data):
    with create_connection() as  conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, data)
                print("Query from execute_query executed successfully")
            except OperationalError as err:
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
        print('check_order', query, data)
        cursor.execute(query, data)
        re_data = cursor.fetchall()
        print("Query from check_order executed successfully")
    except OperationalError as err:
        print(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return re_data


def check_is_exist_in_db(query, data):
    connection = create_connection()
    cursor = connection.cursor()
    result = False
    try:
        cursor.execute(query, data)
        redata = cursor.fetchone()
        print(f"Query from check_is_exist_in_db '{data[0]}' executed successfully")
        if redata is not None:
            result = True
    except OperationalError as err:
        print(f"The ERROR from check_order '{err}' occured ")

    cursor.close()
    connection.close()

    return result


# check_order( query_read_order, ("MP2713064-001", 'Leroy'))


# def get_one_order():
#     connection = create_connection()
#     result, proxy = None, []
#     try:
#         cursor = connection.cursor()
#         cursor.execute(read_new_order)
#         result = cursor.fetchone()
#         print("Fetching single row", result)
#         if result is not None:
#             data = (result[1], result[7])
#             print("Fetching single row-------",data)
#             cursor.execute(read_order_items, data)
#             items = cursor.fetchall()
#             proxy = [item for item in items]
#
#         cursor.close()
#
#     except psycopg2.Error as error:
#         print("Failed to read data from table", error)
#     finally:
#         if connection:
#             connection.close()
#             print("The Sql connection is closed")
#
#     return result, proxy


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

query_update_msg_id = ("UPDATE fresh_bids SET msg_id = %s, dateModifed = NOW() "
                       "WHERE chat_id = %s ")

query_update_contact_id = ("UPDATE fresh_bids SET leads_id = %s, "
                           "contact_id = %s, dateModifed = NOW() "
                       "WHERE chat_id = %s ")

proxy = ("u2i-TOYzRVLyb9Hw_l7u2aBTVg", '4391', "https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/trw_df4110_torm.disk_per.vent.280x24_4_otv_3364311913",
         'e737d71dcddc238d5a1db962f3fb6db9', 353207078, "TRW DF4110 Торм.диск пер.вент.280x24 4 отв",
         True, False, 0, 0)

# maintenans_query(create_fresh_bids)
execute_query_v2(query_write_bid, proxy)