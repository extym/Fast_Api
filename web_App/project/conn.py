import psycopg2
from psycopg2 import OperationalError
from project.conn_maintenance import *


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database='stm_app',
            user='user_name',
            password='user_pass',
            host='localhost',
            port=5432
        )
        print("Connection to DB successfully")

    except OperationalError as error:
        print(f'The ERROR "{error}" occurred')

    return connection


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


query_join = "select * from fresh_orders join order_items oi on fresh_orders.id_mp = oi.id_mp where date_added<'%2023-05-29'"
query_insert = "insert  INTO sales ( mp_order_id, shop_order_id, date_added, shop_name, shipment_date, order_status, shop_status, delivery_type, article, id_1c, quantity,  price )" \
               "VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"


def rewrite_orders(query1, query2):
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

# rewrite_orders(query_join, query_insert)
# # rewrite_orders("select * from fresh_orders  where date_added<'%2023-03-29'")

# maintenans_query(create_fresh_orders_table)
# maintenans_query(create_order_items)
# maintenans_query(create_users)
# maintenans_query(create_market_cred)
# maintenans_query(create_users)
# maintenans_query(create_consult_users)

#
# maintenans_query(create_products)
# # maintenans_query(create_sales)
# maintenans_query(create_attribute_product)
