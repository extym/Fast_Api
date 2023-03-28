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


query_read_order = (" SELECT * from fresh_orders "
                         " WHERE id_mp = %s and shop_name = %s ")


query_write_order = ("INSERT INTO fresh_orders "
    "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
                     "shipment_Date, status, our_status, payment_Type, delivery)"
                     "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

# query_write_order_items = ("INSERT INTO order_items "
#     "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
#                      "shipment_Date, status, our_status, payment_Type, delivery)"
#                      "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

query_rm_full_order = (" SELECT * from fresh_orders, order_items "
                         " WHERE id_mp = %s")

query_write_items = ("INSERT INTO order_items "
    "(id_mp, our_order_id, shop_Name, "
                     "our_status, vendor_code, id_1c, quantity, price)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

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