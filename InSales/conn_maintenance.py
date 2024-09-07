create_product_table = """
CREATE TABLE IF NOT EXISTS goods (
id SERIAL PRIMARY KEY,
shop_id varchar NOT None,
category_id varchar,
parent_category_id varchar,
sub_category_id varchar,
date_Added varchar,
date_Modifed varchar,
vendor_name TEXT,
price varchar,
status TEXT,
vendor_shop_name TEXT, 
sku varchar,
netlab_category_id varchar,
netlab_parent_category_id varchar,
netlab_price TEXT,
netlab_stock INT,
logic_category_id varchar,
logic_parent_category_id varchar, 
logic_price TEXT, 
logic_stock INT,
product_name varchar, 
quantity INT,
UNIQUE (shop_id, vendor_shop_name)
)
"""



query_write_product = ("INSERT INTO goods "
    "(shop_id, date_Added, date_Modifed, vendor_name, price, vendor_shop_name, "
                     "netlab_category_id, product_name, quantity, sku)"
                     "VALUES (%s, NOW(), NOW(), %s, %s, %s, %s, %s, %s, %s)")

query_write_vendors = ("INSERT INTO vendors "
    "(vendor_name, category_name, category_id, date_Added, date_Modifed, "
                     "parent_category_id)"
                     "VALUES (%s, %s, %s, NOW(), NOW(), %s)")

query_write_vendors_v2 = ("INSERT INTO vendors "
    "(vendor_name, category_name, category_id, date_Added, date_Modifed, "
                     "parent_category_id, leaf )"
                     "VALUES (%s, %s, %s, NOW(), NOW(), %s, %s)")


query_write_site_categories = ("INSERT INTO site_categories "
                               "( site_name, category_id, category_name, date_Added, date_Modifed, "
                               "parent_category_id, how_position, site_path, vendor_name_category)"
                               "VALUES (%s, %s, %s, NOW(), NOW(), %s, %s, %s, %s)")


query_write_site_categories_v2 = ("INSERT INTO site_categories "
                               "( site_name, category_id, category_name, date_Added, date_Modifed, "
                               "parent_category_id, how_position, site_path, vendor_name_category)"
                               "VALUES (%s, %s, %s, NOW(), NOW(), %s, %s, %s, %s) "
                                  "ON CONFLICT (category_id, vendor_name_category) do update SET "
                                  " (site_name, category_name, date_Modifed, parent_category_id, how_position, site_path)"
                                  " = (excluded.site_name, excluded.category_name, now(), excluded.parent_category_id, "
                                  " excluded.how_position, excluded.site_path)")


query_write_site_categories_v3 = ("INSERT INTO site_categories "
                               "( site_name, category_id, category_name, date_Added, date_Modifed, "
                               "parent_category_id, how_position, site_path, vendor_name_category)"
                               "VALUES (%s, %s, %s, NOW(), NOW(), %s, %s, %s) ")





query_update_site_categories = ("UPDATE site_categories SET category_name = %s, date_Modifed = NOW(),"
                                " parent_category = %s, how_position = %s, site_path = %s"
                               " WHERE category_id = %s  and vendor_name_category = %s ")


create_vendors_table = """
CREATE TABLE IF NOT EXISTS vendors (
id SERIAL PRIMARY KEY,
vendor_name varchar NOT NULL,
category_name varchar,
category_id varchar,
date_Added varchar,
date_Modifed varchar,
parent_category_id varchar,
leaf boolean, 
site_category TEXT,
UNIQUE(category_id)
)
"""


create_vendors_table_name = """
CREATE TABLE IF NOT EXISTS logic (
id SERIAL PRIMARY KEY,
vendor_name varchar NOT NULL,
category_name varchar,
category_id varchar,
date_Added varchar,
date_Modifed varchar,
parent_category_id varchar,
leaf boolean, 
site_category TEXT,
UNIQUE(category_id)
)
"""


create_site_categories_table = """
CREATE TABLE IF NOT EXISTS site_categories (
id SERIAL PRIMARY KEY,
site_name varchar NOT NULL,
category_name varchar,
category_id INT,
date_Added varchar,
date_Modifed varchar,
parent_category_id varchar,
leaf boolean, 
parent_category TEXT,
how_position INT,
vendor_name_category TEXT,
vendor_id_category INT,
site_path varchar(510),
group_id int,
UNIQUE(category_id, vendor_name_category)
)
"""



create_order_items = """
CREATE TABLE IF NOT EXISTS order_items (
    id_mp varchar NOT NULL,
    FOREIGN KEY (id_mp)
        REFERENCES goods (id_mp)
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


read_path_categories = ("SELECT site_path, vendor_id_category FROM site_categories"
                        " WHERE vendor_name_category = %s ")


query_read_order = (" SELECT * from goods "
                         " WHERE id_mp = %s and shop_name = %s ")


query_read_category = ("SELECT * from vendors"
                       " WHERE vendor_name = %s and parent_category_id = %s ")


query_read_need_category = ("SELECT vendor_id_category from site_categories"
                       " WHERE vendor_name_category = %s and vendor_id_category is not null ")

query_rewrite_id_marwel = ("SELECT category_id, leaf from vendors"
                       " WHERE vendor_name = %s ")

# query_read_need_category_v2 = ( f"SELECT vendor_id_category from {vendor}"
#                        " WHERE vendor_name = %s ")


query_get_actual_cats = ("SELECT vendor_id_category, category_name, site_path FROM site_categories "
                         " WHERE vendor_id_category is not null")

query_get_actual_cats_v3 = ("SELECT vendor_id_category, category_name, site_path, category_id, group_id, leaf FROM site_categories "
                         " WHERE vendor_id_category != '0' and vendor_name_category = %s ")

query_get_actual_cats_v2 = ("SELECT vendor_id_category, category_name, site_path, category_id, group_id FROM site_categories "
                         " WHERE vendor_id_category != '0' and vendor_name_category = %s ")


query_update_from_file = ("UPDATE site_categories SET vendor_id_category = %s, group_id = %s "
            "WHERE id = %s AND vendor_name_category = %s")


query_write_order_items = ("INSERT INTO order_items "
    "(id_mp, our_id, date_Added, date_Modifed, shop_Name, "
                     "shipment_Date, status, our_status, payment_Type, delivery)"
                     "VALUES (%s, %s, NOW(), NOW(), %s, %s, %s, %s, %s, %s)")

query_rm_full_order = (" SELECT * from goods, order_items "
                         " WHERE id_mp = %s")

query_write_items = ("INSERT INTO goods "
    "(shop_id, category_id, shop_Name, "
                     "our_status, vendor_code, id_1c, quantity, price)"
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

query_read_items = (" SELECT * from order_items "
                    " WHERE id_ip = %s and shop_name = %s ")

read_new_order = (" SELECT * from goods "
                    " WHERE our_status = 'NEW' ")

read_order_items = (" SELECT * from order_items "
                    " WHERE id_mp = %s and shop_name = %s ")


update_send_data_order = (" UPDATE goods SET dateSendData = NOW(), dateModifed = NOW(), ourStatus = 'SEND_TO_1C' "
                          " WHERE id_MP = %s and shop_name = %s ")


update_status_order = (" UPDATE goods "
                       "SET status = %s, our_status = %s "
                       "WHERE id_MP = %s and shop_name = %s ")


update_status_order_reverse_id = (" UPDATE goods "
                       "SET status = %s, our_status = %s "
                       "WHERE our_id = %s and shop_name = %s ")


rewrite_status_order = (" UPDATE goods "
                       "SET status = %s "
                       "WHERE id_MP = %s and shop_name = %s ")

rebase_order = (" UPDATE goods "
               "SET our_status = %s "
               "WHERE id = %s and id_MP = %s ")


strong_rebase_order = (" INSERT INTO send_orders "
    "(id_mp, our_order_id, shop_Name, our_status, vendor_code, id_1c, quantity, price)"
    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")