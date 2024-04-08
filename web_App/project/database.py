import psycopg2
#apt install python<version>-dev
#pip install psycopg2-binary

def connect():
    conn = psycopg2.connect(host='localhost',
                            database='stm_app',
                            user='user_name',
                            password='user_pass')
    # conn = psycopg2.connect(host='localhost',
    #                         database='bots',
    #                         user='user_bot',
    #                         password='bot_pass')
    print("connect")
    return conn

# connect()

class Data_base_connect():

    def __init__(self):

        self.host = 'localhost',
        self.database = 'stm_app',
        self.user = 'user_name',
        self.password = 'user_pass',
        # self.host = 'localhost',
        # self.database = 'bots',
        # self.user = 'bots',
        # self.password = 'bot_pass',
        # self.port = 5432
        self.conn = None,
        self.curs = None
        # try:
        self.conn = psycopg2.connect(host='localhost',
                            database='stm_app',
                            user='user_name',
                            password='user_pass')
        # self.conn = psycopg2.connect(host='localhost',
        #                     database='bots',
        #                     user='bots',
        #                     password='bot_pass')
        print('connect success')


    def select_smth(self, to_from, data):
        self.curs = self.conn.cursor()
        self.curs.execute(" SELECT FROM %s WHERE id = `%s` ", (to_from, data))
        datas = self.curs.fetchall()
        self.curs.close()

        return datas


    def select_shop_name(self, company_id):
        self.curs = self.conn.cursor()
        self.curs.execute(" SELECT shop_name, name_mp FROM marketplaces WHERE company_id = %s ", (company_id,))
        datas = self.curs.fetchall()
        self.curs.close()
        print(3454, datas)
        return datas



    def insert_new_mp(self, uid, shop_id, shop_name, mp, key, company_id):
        self.conn.autocommit=True
        self.curs = self.conn.cursor()
        self.curs.execute("INSERT INTO marketplaces (user_id, seller_id, shop_name, name_mp, key_mp, company_id, date_added)"
                          "values (%s, %s, %s, %s, %s, %s, NOW())", (uid, shop_id, shop_name, mp, key, company_id))
        self.curs.close()

    def update_mp(self, uid, shop_id, shop_name, mp, key, company_id):
        # self.conn.autocommit=True
        # self.curs = self.conn.cursor()
        # self.curs.execute("UPDATE marketplaces (user_id, seller_id, shop_name, name_mp, key_mp, company_id, date_added)"
        #                   "values (%s, %s, %s, %s, %s, %s, NOW())", (uid, shop_id, shop_name, mp, key, company_id))
        # self.curs.close()
        pass


    def insert_new_product(self, uid, shop_id, shop_name, mp, key):
        self.conn.autocommit=True
        self.curs = self.conn.cursor()
        self.curs.execute(" INSERT INTO products (articul_product, shop_name, company_id, quantity, price_product_base, discount, description_product, photo, category, id_1c, date_added, date_modifed, selected_mp, name_product, status_mp, images_product, price_add_k, discount_mp_product, set_shop_name, external_sku, alias_prod_name, status_in_shop, photo_line, shop_k_product, discount_shop_product, quantity_for_shop, description_product_add, uid_edit_user, final_price) VALUES (%(articul_product)s, %(shop_name)s, %(company_id)s, %(quantity)s, %(price_product_base)s, %(discount)s, %(description_product)s, %(photo)s, %(category)s, %(id_1c)s, %(date_added)s, %(date_modifed)s, %(selected_mp)s, %(name_product)s, %(status_mp)s, %(image_product)s, %(price_add_k)s, %(discount_mp_product)s, %(set_shop_name)s, %(external_sku)s, %(alias_prod_name)s, %(status_in_shop)s, %(photo_line)s, %(shop_k_product)s, %(discount_shop_product)s, %(quantity_for_shop)s, %(description_product_add)s, %(uid_edit_user)s, %(final_price)s) RETURNING products.id", (uid, shop_id, shop_name, mp, key))
        self.curs.close()


    def select_orders_from_id(self, seller_id):
        self.curs = self.conn.cursor()
        self.curs.execute("select * from `fresh_orders` where `seller_id`=s%", (seller_id))
        raw_orders = self.curs.fetchall()

        return raw_orders

    def select_orders(self):
        self.curs = self.conn.cursor()
        self.curs.execute("select * from fresh_orders ")
        raw_orders = self.curs.fetchall()
        self.curs.close()

        return raw_orders
    
    
    def insert_key_mp(self, seller_id, name_mp, shop_name, id_mp, key_mp):
        self.conn.autocommit=True
        self.curs = self.conn.cursor()
        self.curs.execute("INSERT INTO marketplaces "
                          " (user_id, seller_id, shop_name, id_sell_mp, key_mp, date_added, date_modifed )"
                          "VALUES (%s, %s, %s, %s, %s, NOW(), NOW())", (seller_id, name_mp, shop_name,  id_mp, key_mp))