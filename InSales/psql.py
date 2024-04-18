import psycopg2


class PgDatabase:
    def __init__(self, host=None, user=None, password=None, database=None):
        self.user = user
        self.host = host
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None

        self.conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=5432
        )
        # self.cursor = self.conn.cursor()

        print('PSQL cursor opened')

    def get_seller_id_category(self):
        self.cursor = self.conn.cursor()
        raw_list = []
        # try:
        self.cursor.execute("SELECT * from site_categories")
        raw_list = self.cursor.fetchall()
        self.cursor.close()

        # except:
        #     self.cursor.execute("ROLLBACK")
        #     print('ERROR_GET_SITE_CATEGORIES')

        return raw_list

    def get_seller_id_category_v2(self, vendor_name):
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM site_categories WHERE vendor_name_category=%s", (vendor_name,))
        raw_list = self.cursor.fetchall()
        self.cursor.close()
        # print('raw_list', raw_list)
        return raw_list

    def get_vendor_id_categoies(self, name_vendor):
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM vendors WHERE vendor_name=%s", (name_vendor,))
        raw_list = self.cursor.fetchall()
        self.cursor.close()

        return raw_list

    def get_vendor_id_categoies_v2(self, name_vendor):
        raw_list = []
        self.cursor = self.conn.cursor()
        if name_vendor == 'netlab':
            self.cursor.execute("SELECT * FROM vendors WHERE vendor_name=%s", (name_vendor,))
            raw_list = self.cursor.fetchall()
        elif name_vendor == 'logic':
            self.cursor.execute("SELECT * FROM logic WHERE vendor_name=%s", (name_vendor,))
            raw_list = self.cursor.fetchall()
        self.cursor.close()

        return raw_list

    def get_vendor_id_categoies_v3(self, name_vendor):
        raw_list = []
        self.cursor = self.conn.cursor()
        if name_vendor == 'netlab':
            self.cursor.execute("SELECT * FROM vendors WHERE vendor_name=%s", (name_vendor,))
            raw_list = self.cursor.fetchall()
        elif name_vendor == 'logic':
            self.cursor.execute("SELECT * FROM logic WHERE vendor_name=%s", (name_vendor,))
            raw_list = self.cursor.fetchall()
        self.cursor.close()

        return raw_list

    def update_site_delive(self, name_vendor: str, category_id: int, new_category_id):
        self.cursor = self.conn.cursor()
        result = False
        if name_vendor == 'netlab':
            # try:
            self.cursor.execute(
                "UPDATE site_categories SET vendor_id_category = %s "
                "WHERE id = %s AND vendor_name_category = %s",
                (new_category_id, category_id, name_vendor))
            print(33333, new_category_id, category_id, name_vendor)
            self.conn.commit()
            self.cursor.close()
            print(11111, type(new_category_id), type(category_id), type(name_vendor))
            result = True
            #     print('ALL_RIDE_WRITE_CAT')
            # except:
            #     print('FUCK_UP_WRITE_CAT')
        elif name_vendor == 'logic':
            self.cursor.execute(
                "UPDATE site_categories SET vendor_id_category = %s "
                "WHERE id = %s AND vendor_name_category = %s",
                (new_category_id, category_id, name_vendor))
            print(44444, new_category_id, category_id, name_vendor)
            self.conn.commit()
            self.cursor.close()
            print(55555, type(new_category_id), type(category_id), type(name_vendor))
            result = True
            #     print('ALL_RIDE_WRITE_CAT')
            # except:
            #     print('FUCK_UP_WRITE_CAT')

        return result

    def update_site_delive_v2(self, name_vendor: str, category_id: int, new_category_id: str):
        self.cursor = self.conn.cursor()
        result = False
        # if name_vendor == 'netlab':
        #     # try:
        #     self.cursor.execute(
        #         "UPDATE site_categories SET vendor_id_category = %s "
        #         "WHERE id = %s AND vendor_name_category = %s",
        #         (new_category_id, category_id, name_vendor))
        #     self.conn.commit()
        #     self.cursor.close()
        #     result = True
        #     #     print('ALL_RIDE_WRITE_CAT')
        #     # except:
        #     #     print('FUCK_UP_WRITE_CAT')
        # elif name_vendor == 'logic':
        #     self.cursor.execute(
        #         "UPDATE site_categories SET vendor_id_category = %s "
        #         "WHERE id = %s AND vendor_name_category = %s",
        #         (new_category_id, category_id, name_vendor))
        #     self.conn.commit()
        #     self.cursor.close()
        #     result = True
        #     #     print('ALL_RIDE_WRITE_CAT')
        #     # except:
        #     #     print('FUCK_UP_WRITE_CAT')
        #
        # else:
        self.cursor.execute(
            "UPDATE site_categories SET vendor_id_category = %s "
            "WHERE id = %s AND vendor_name_category = %s",
            (new_category_id, category_id, name_vendor))
        print(77777, new_category_id, category_id, name_vendor)
        self.conn.commit()
        self.cursor.close()
        print(55555, type(new_category_id), type(category_id), type(name_vendor))
        result = True
        #     print('ALL_RIDE_WRITE_CAT')
        # except:
        #     print('FUCK_UP_WRITE_CAT')

        return result

    def update_site_cats_from_file(self, name_vendor: str, category_id: int,
                                   new_category_id: str, group_id: int):
        self.cursor = self.conn.cursor()
        result = False
        self.cursor.execute(
            "UPDATE site_categories SET vendor_id_category = %s, group_id = %s "
            "WHERE id = %s AND vendor_name_category = %s",
            (new_category_id, group_id, category_id, name_vendor))
        print(77777, new_category_id, category_id, name_vendor)
        self.conn.commit()
        self.cursor.close()
        print(55555, type(new_category_id), type(category_id), type(name_vendor))
        result = True
        #     print('ALL_RIDE_WRITE_CAT')
        # except:
        #     print('FUCK_UP_WRITE_CAT')

        return result


    def update_categories_from_site(self, vendor: str):
        self.cursor = self.conn.cursor()
        self.cursor.executemany(
            "UPDATE site_categories SET category_name = %s, date_Modifed = NOW(),"
            " parent_category = %s, how_position = %s, site_path = %s"
            " WHERE category_id = %s  and vendor_name_category = %s "
        )

    def get_site_categories(self):
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT id, category_name, category_id,"
                            "parent_category_id, vendor_name_category FROM site_categories ")
        raw_list = self.cursor.fetchall()
        self.cursor.close()
        # print(raw_list)

        return raw_list

    # def insert_update_dict(self, table, id: str, name: str, meta: Dict):
    #     try:
    #         meta = json.dumps(meta)
    #         self.cur.execute(f"INSERT INTO `{table}` (`id`, `name`, `meta`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `name` = %s, `meta` = %s", (id, name, meta, name, meta))
    #         self.conn.commit()
    #     except Exception as e:
    #         logging.warning(f'MySQL insert/update dict table {table} error')
    #         print(e)
    #         return False
    #     return True
