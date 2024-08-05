import psycopg2
from psycopg2 import OperationalError, IntegrityError
from conn_maintenance import *
from psycopg2.errors import UniqueViolation


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            database='insales',
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
        # print("Query from execute_query executed successfully")

    except OperationalError as err:
        print(f"The ERROR from execute_query '{err}' occured ")

    cursor.close()
    connection.close()


def execute_query_return(query, data: str):
    connection = create_connection()
    cursor = connection.cursor()
    # try:
    cursor.execute(query, data)
    raw_list = cursor.fetchall()
    # print("Query from execute_query executed successfully", type(raw_list))
    #
    # except OperationalError as err:
    #     print(f"The ERROR from execute_query '{err}' occured ")
    #     result = []
    cursor.close()
    connection.close()
    # print(raw_list)
    return raw_list


def execute_query_return_v2(query):
    connection = create_connection()
    cursor = connection.cursor()
    # try:
    cursor.execute(query)
    raw_list = cursor.fetchall()
    # print("Query from execute_query executed successfully", type(raw_list))
    #
    # except OperationalError as err:
    #     print(f"The ERROR from execute_query '{err}' occured ")
    #     result = []
    cursor.close()
    connection.close()
    # print(raw_list)
    return raw_list


# execute_query_return(read_path_categories, ('netlab',))

async def execute_query_update(data):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    result = False
    for row in data:
        try:
            # print(777777777777, row)
            cursor.execute(query_write_site_categories_v2, row)
            # print("Query from execute_update_query executed successfully")
            result = True
        except OperationalError as err:
                cursor.execute(query_update_site_categories, row)
                print(f"The ERROR from execute_query '{err}' occured ")
        # else :
        #     print('FUCK_UP_222')

    cursor.close()
    connection.close()

    return result


async def executemany_query(query, data):
    connection = create_connection()
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.executemany(query, data)
        # print("Query from execute_many_query executed successfully")
        result = True
    except OperationalError as err:
        print(f"The ERROR from execute_many_query '{err}' occurred ")
        result = False
    except IntegrityError as e:
            if isinstance(UniqueViolation):
                print('DUPLICATE_key_error')
            result = False
    cursor.close()
    connection.close()

    return result


def execute_query_return_id(connection, query, data):
    connection.autocommit = True
    cursor = connection.cursor()
    lastrowid = None
    try:
        cursor.execute(query, data)
        lastrowid = cursor.lastroid()
        # print("Query from execute_query_return_id executed successfully")

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
        # print("Query from check_order executed successfully")
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
        # print(f"Query from check_is_exist_in_db '{data[0]}' executed successfully")
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
            print("Fetching single row-------",data)
            cursor.execute(read_order_items, data)
            items = cursor.fetchall()
            proxy  = [item for item in items]

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

# maintenans_query(create_product_table)
# maintenans_query(create_order_items)
# maintenans_query(create_vendors_table)
# maintenans_query(create_site_categories_table)
# maintenans_query(create_vendors_table_name)

