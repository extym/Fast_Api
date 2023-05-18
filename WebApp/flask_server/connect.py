import psycopg2

def connect():
    conn = psycopg2.connect(host='localhost',
                            database='stm_app',
                            user='user_name',
                            password='user_pass')
    print("connect")
    return conn

# connect()

class Data_base_connect():

    def __init__(self):

        self.host = 'localhost',
        self.database = 'stm_app',
        self.user = 'user_name',
        self.password = 'user_pass',
        self.port = 5432
        self.conn = None,
        self.curs = None
        # try:
        self.conn = psycopg2.connect(host='localhost',
                            database='stm_app',
                            user='user_name',
                            password='user_pass')
        print('connect success')


    def select_smth(self, to_from, data):
        self.conn.autocommit=True
        self.curs = self.conn.cursor()
        datas = self.curs.execute("SELECT FROM `s%` WHERE `id=%s`", (to_from, data))
        self.curs.close()

        return datas

    def insert_new_mp(self, uid, shop_id, shop_name, mp, key):
        self.conn.autocommit=True
        self.curs = self.conn.cursor()
        self.curs.execute("INSERT INTO marketplaces (user_id, seller_id, shop_name, name_mp, key_mp, date_added)"
                          "values (%s, %s, %s, %s, %s, NOW())", (uid, shop_id, shop_name, mp, key))
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