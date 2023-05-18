# -- coding: utf-8 --
"""
Database class
"""
import datetime
import logging
import json
from typing import Any, Dict, List

import mysql.connector
# pip install mysql-connector-python

from settings import OZON_ORDERS_OLD_DAYS


class MsDatabase:
    def __init__(self, host=None, user=None, passwd=None, database=None):
        self.user = user
        self.host = host
        self.passwd = passwd
        self.database = database
        self.conn = None
        self.cur = None
        # try:
        self.conn = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
        self.cur = self.conn.cursor(buffered=True)
        # except Exception as ex:
        #     print(f'MySQL connection error {ex}')
        #     logging.warning('MySQL connection error')
        # else:
        print('MySQL cursor opened')
        logging.info('MySQL cursor opened')

    def reconnect(self):
        self.conn.close()
        self.cur.close()
        self.conn = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        self.cur = self.conn.cursor()
        logging.info('MySQL cursor reopened')

    def insert_new_seller(self, seller_name, seller_client_id, seller_token):
        # self.cur.execute(
        #     "INSERT INTO `sellers` (name, client_id, token) VALUES (%s, %s, %s)",
        #     (seller_name, seller_client_id, seller_token))
        # self.conn.commit()
        try:
            self.cur.execute("INSERT INTO `sellers` (name, client_id, token) VALUES (%s, %s, %s)", (seller_name, seller_client_id, seller_token))
            self.conn.commit()
        except:
            logging.warning(f'MySQL add seller {seller_name} error')
            print(f'MySQL add seller {seller_name} error')
            return False
        return True

    def update_seller(self, seller: Dict):
        try:
            self.cur.execute("UPDATE `sellers` SET `name`=%s, `token`=%s, date_ozon_field=%s, `status`=%s, `contragent`=%s, `comment`=%s, `active`=%s, `fb`=%s, `sklad`=%s, `organization`=%s, `ozon_store`=%s, `usluga`=%s, `usluga_price_ms`=%s, `status_realfbs`=%s, `contragent_realfbs`=%s, `comment_realfbs`=%s, `usluga_realfbs`=%s, `usluga_price_ms_realfbs`=%s, `price`=%s, `cancell_status`=%s WHERE `client_id`=%s",
                             (seller['name'], seller['token'], seller['date_ozon_field'], seller['status'], seller['contragent'], seller['comment'], seller['active'], '', seller['sklad'], seller['organization'], seller['ozon_store'], seller['usluga'], seller['usluga_price_ms'], seller['status_realfbs'], seller['contragent_realfbs'], seller['comment_realfbs'], seller['usluga_realfbs'], seller['usluga_price_ms_realfbs'], seller['price'], seller['cancell_status'], seller['client_id']))
            self.conn.commit()
        except Exception as ex:
            print(f"MySQL update seller {seller['name']} error {ex}")
            logging.warning(f"MySQL update seller {seller['name']} error")
            return False
        return True

    def truncate_table(self, table: str):
        try:
            self.cur.execute(f"TRUNCATE TABLE IF EXISTS `{table}`")
            self.conn.commit()
        except:
            print(f'MySQL clear table {table} error')
            logging.warning(f'MySQL clear table {table} error')
            return False
        return True

    def get_all_sellers(self):
        self.cur.execute(f"SELECT * FROM `sellers`")
        raw_list = self.cur.fetchall()
        return raw_list

    def get_all_sellers_today(self, client_id):
        raw_list = []
        for client in client_id:
            self.cur.execute(f"SELECT * FROM `sellers` WHERE `client_id`=%s", (client,))
            raw_list += self.cur.fetchall()
        return raw_list

    def get_active_sellers_id_token(self):
        self.cur.execute(f"SELECT `client_id`, `token` FROM `sellers` WHERE `active`=1")
        raw_list = self.cur.fetchall()
        return raw_list

    def get_active_sellers_all(self):
        self.cur.execute(f"SELECT * FROM `sellers` WHERE `active`=1")
        raw_list = self.cur.fetchall()
        return raw_list

    def get_seller(self, client_id):
        self.cur.execute(f"SELECT * FROM `sellers` WHERE `client_id`=%s", (client_id,))
        raw_list = self.cur.fetchall()
        return raw_list

    def get_dict(self, table='organizations'):
        res = {}
        try:
            self.cur.execute(f"SELECT `id`, `name` FROM `{table}` ORDER BY `name`")
            raw_list = self.cur.fetchall()
        except:
            return res
        for elem in raw_list:
            try:
                res[elem[0]] = elem[1]
            except:
                continue
        return res

    def get_dict_id_meta(self, table, id: str) -> Dict:
        res = {}
        try:
            self.cur.execute(f"SELECT `meta` FROM `{table}` WHERE `id` = %s", (id,))
            raw = self.cur.fetchone()
            res = json.loads(raw)
        except:
            return res

        return res

    def insert_update_dict(self, table, id: str, name: str, meta: Dict):
        try:
            meta = json.dumps(meta)
            self.cur.execute(f"INSERT INTO `{table}` (`id`, `name`, `meta`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `name` = %s, `meta` = %s", (id, name, meta, name, meta))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert/update dict table {table} error')
            print(e)
            return False
        return True

    def insert_update_ozon_product(self, seller_id: str, product_dict: Dict):
        try:
            self.cur.execute(
                f"INSERT INTO `ozon_products` (`product_id`, `offer_id`, `name`, `client_id`, `barcode`) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `offer_id` = %s, `name` = %s, `barcode` = %s",
                (product_dict['id'], product_dict['offer_id'], product_dict['name'], seller_id, product_dict['barcode'], product_dict['offer_id'], product_dict['name'], product_dict['barcode']))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert/update dict table ozon_products error')
            print(e)
            return False
        return True

    def update_ozon_product_link(self, client_id: str, product_id: int, ms_id: str):
        try:
            self.cur.execute(
                f"UPDATE `ozon_products` SET `ms_id` = %s WHERE `client_id` = %s AND `product_id` = %s",
                (ms_id, client_id, product_id))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL update dict table ozon_products LINK error')
            print(e)
            return False
        return True

    def update_ozon_delive(self, client_id: str, product_id: int, delive: float):
        try:
            self.cur.execute(
                f"UPDATE `ozon_products` SET `delive` = %s WHERE `client_id` = %s AND `product_id` = %s",
                (delive, client_id, product_id))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL update dict table ozon_products delive error')
            print(e)
            return False
        return True

    def insert_update_ms_product(self, product: List):
        # product[4] = json.dumps(product[4])
        # self.cur.execute(
        #     f"INSERT INTO `ms_products` (`id`, `name`, `code`, `article`, `barcodes`) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `name` = %s, `code` = %s, `article` = %s, `barcodes` = %s",
        #     (
        #     product[0], product[1], product[2], product[3], product[4], product[1], product[2], product[3], product[4]))
        # self.conn.commit()
        try:
            product[4] = json.dumps(product[4])
            self.cur.execute(
                f"INSERT INTO `ms_products` (`id`, `name`, `code`, `article`, `barcodes`) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `name` = %s, `code` = %s, `article` = %s, `barcodes` = %s",
                (product[0], product[1], product[2], product[3], product[4], product[1], product[2], product[3], product[4]))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert/update dict table ms_products error')
            print(e)
            return False
        return True

    def insert_update_oder(self, client_id: str, ms_order_id: str, order: Dict, product: Dict, comment: str, ms_order_href: str, label: int, fbs: int):
        try:
            delivery_date_end = order['analytics_data']['delivery_date_end']
            if delivery_date_end is None:
                delivery_date_end = ''
        except:
            delivery_date_end = ''
        try:
            self.cur.execute(
                f"INSERT INTO `orders` (`client_id`, `posting_number`, `order_id`, `status`, `shipment_date`, `warehouse_id`, `ms_order_id`, `product_offer_id`, `product_ms_href`, `product_quantity`, `product_price`, `comment`, `ms_order_href`, `label`, `fbs`, `delivery_date_end`) "
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `status` = %s, `shipment_date` = %s, `ms_order_id` = %s, `ms_order_href` = %s, `label` = %s, `fbs` = %s, `delivery_date_end` = %s",
                (client_id, order['posting_number'], order['order_id'], order['status'], order['shipment_date'],
                 order['delivery_method']['warehouse_id'], ms_order_id, product['offer_id'], product['href'],
                 product['quantity'], product['price'], '', ms_order_href, label, fbs, delivery_date_end,
                 order['status'], order['shipment_date'], ms_order_id, ms_order_href, label, fbs, delivery_date_end))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert/update order error')
            print(e)
            return False
        return True

    def get_products(self, client_id):
        try:
            self.cur.execute("SELECT `product_id`, `offer_id`, `name`, `barcode`, `ms_id`, `delive` FROM `ozon_products` WHERE `client_id` = %s ORDER BY `name`", (client_id, ))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_product_href(self, client_id, offer_id):
        try:
            self.cur.execute("SELECT `ms_id` FROM `ozon_products` WHERE `client_id` = %s AND `offer_id` = %s", (client_id, offer_id))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_product_href_delive(self, client_id, offer_id):
        try:
            self.cur.execute("SELECT `ms_id`, `delive` FROM `ozon_products` WHERE `client_id` = %s AND `offer_id` = %s", (client_id, offer_id))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_ms_products(self):
        try:
            self.cur.execute("SELECT `id`, `name`, `code`, `article` FROM `ms_products` ORDER BY `name`")
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_order_ms_id(self, client_id, posting_number):
        try:
            self.cur.execute("SELECT `ms_order_id`, `ms_order_href` FROM `orders` WHERE `client_id` = %s AND `posting_number` = %s", (client_id, posting_number))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_order_id_href_label(self, client_id, posting_number):
        try:
            self.cur.execute("SELECT `ms_order_id`, `ms_order_href`, `label` FROM `orders` WHERE `client_id` = %s AND `posting_number` = %s", (client_id, posting_number))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_order_comment(self, client_id, posting_number):
        try:
            self.cur.execute("SELECT `comment` FROM `orders` WHERE `client_id` = %s AND `posting_number` = %s", (client_id, posting_number))
            raw_list = self.cur.fetchone()
        except:
            return []
        return raw_list

    def get_order_status(self, client_id, posting_number):
        try:
            self.cur.execute("SELECT `status` FROM `orders` WHERE `client_id` = %s AND `posting_number` = %s", (client_id, posting_number))
            raw_list = self.cur.fetchone()
        except:
            return []
        return raw_list

    def get_order_href_status(self, client_id, posting_number):
        try:
            self.cur.execute("SELECT `ms_order_href`, `status` FROM `orders` WHERE `client_id` = %s AND `posting_number` = %s", (client_id, posting_number))
            raw_list = self.cur.fetchone()
        except:
            return []
        return raw_list

    def get_last_orders_href(self, client_id, period=OZON_ORDERS_OLD_DAYS, status=None):
        try:
            if status:
                self.cur.execute("SELECT `ms_order_href` FROM `orders` WHERE `client_id` = %s AND `status` = %s AND date > CURDATE() - INTERVAL %s DAY", (client_id, status, period))
            else:
                self.cur.execute("SELECT `ms_order_href` FROM `orders` WHERE `client_id` = %s AND date > CURDATE() - INTERVAL %s DAY", (client_id, period))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_fbs_orders_href_wo_demand(self, client_id, period=OZON_ORDERS_OLD_DAYS):
        # ms_demand: 0 - по умолчанию, 1 - не собран, 2 - не отгружен, 3 - отгружен
        try:
            self.cur.execute("SELECT `ms_order_href` FROM `orders` WHERE `client_id` = %s AND date > CURDATE() - INTERVAL %s DAY AND `fbs` = 1 AND `ms_demand` != 3", (client_id, period))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_orders_w_labels_to_date(self, client_id, ms_date_from: str, ms_date_to: str):
        # ms_date_list_from = ms_date_from.split('.')
        # mysql_date_from = f'"{ms_date_list_from[2]}-{ms_date_list_from[1]}-{ms_date_list_from[0]}"'
        # ms_date_list_to = ms_date_to.split('.')
        # mysql_date_to = f'"{ms_date_list_to[2]}-{ms_date_list_to[1]}-{ms_date_list_to[0]}"'
        mysql_timestamp_from = datetime.datetime.strptime(ms_date_from + ' 00:00:01', "%d.%m.%Y %H:%M:%S").timestamp()
        mysql_timestamp_to = datetime.datetime.strptime(ms_date_to + ' 23:59:59', "%d.%m.%Y %H:%M:%S").timestamp()
        # print(
        #     'SELECT `posting_number`, `ms_order_href` FROM `orders` WHERE `client_id` = %s AND `label` = 1 AND `add_date` >= %s AND `add_date` <= %s' %
        #     (client_id, mysql_timestamp_from, mysql_timestamp_to))
        # self.cur.execute(
        #     'SELECT `posting_number`, `ms_order_href` FROM `orders` WHERE `client_id` = %s AND `label` = 1 AND unix_timestamp(add_date) >= %s AND unix_timestamp(add_date) <= %s' %
        #     (client_id, mysql_timestamp_from, mysql_timestamp_to))
        # raw_list = self.cur.fetchall()
        try:
            self.cur.execute('SELECT `posting_number`, `ms_order_href` FROM `orders` WHERE `client_id` = %s AND `label` = 1 AND unix_timestamp(add_date) >= %s AND unix_timestamp(add_date) <= %s' %
            (client_id, mysql_timestamp_from, mysql_timestamp_to))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_order_posting_number_by_href(self, client_id, ms_order_href):
        try:
            self.cur.execute("SELECT `posting_number` FROM `orders` WHERE `client_id` = %s AND `ms_order_href` = %s", (client_id, ms_order_href))
            raw_list = self.cur.fetchone()
        except:
            return []
        return raw_list

    def update_oder_status(self, client_id: str, posting_number: str, status: str):
        try:
            self.cur.execute(
                f"UPDATE `orders` SET `status` = %s WHERE `client_id` = %s AND `posting_number` = %s", (status, client_id, posting_number))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL update order status error')
            print(e)
            return False
        return True

    def update_oder_demand(self, client_id: str, ms_href: str, demand: int):
        # ms_demand: 0 - по умолчанию, 1 - не собран, 2 - не отгружен, 3 - отгружен
        # self.cur.execute(
        #     f"UPDATE `orders` SET `ms_demand` = %s WHERE `client_id` = %s AND `ms_order_herf` = %s",
        #     (demand, client_id, ms_href))
        # self.conn.commit()
        try:
            self.cur.execute(
                f"UPDATE `orders` SET `ms_demand` = %s WHERE `client_id` = %s AND `ms_order_href` = %s", (demand, client_id, ms_href))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL update order demand error')
            print(e)
            return False
        return True
        
    def get_order_order_demand_assembled(self):
        try:
            self.cur.execute(
                f"SELECT * FROM `orders` WHERE `ms_demand` = %s AND `fbs` = %s", (1, 1)
            )
            raw_list = self.cur.fetchall()
            return raw_list
        except Exception as e:
            print(e)
            return False
        
    def get_all_orders(self):
        try:
            self.cur.execute(
                f"SELECT * FROM `orders`"
            )
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(e)
            return False

    def get_orders_date_by_status(self, client_id, status):
        try:
            self.cur.execute("SELECT `posting_number`, `delivery_date_end` FROM `orders` WHERE `client_id` = %s AND `status` = %s", (client_id, status))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_seller_orders(self, client_id):
        try:
            self.cur.execute("SELECT `posting_number`, `date`, `status`, `ms_order_id`, `label`, `fbs`, `delivery_date_end`, `add_date`, `ms_demand` FROM `orders` WHERE `client_id` = %s ORDER BY `add_date` DESC, `date` DESC", (client_id,))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_seller_acts(self, client_id):
        try:
            self.cur.execute("SELECT `act_id`, `date_create`, `date_update`, `status`, `file_name`, `file_name_edo`, `ms_demand` FROM `acts` WHERE `client_id` = %s ORDER BY `date_update` DESC", (client_id,))
            raw_list = self.cur.fetchmany(size=30)
        except:
            return []
        return raw_list

    def get_seller_acts_v2(self, client_id):
        try:
            self.cur.execute("SELECT `act_id`, `date_create`, `date_update`, `status`, `file_name`, `file_name_edo`, `ms_demand` FROM `acts` WHERE `client_id` = %s ORDER BY `date_create` DESC", (client_id,))
            raw_list = self.cur.fetchmany(size=30)
        except:
            return []
        return raw_list

    def get_seller_acts_v3(self):
        proxy = []
        # try:
            # for client_id in list_client_id:
        self.cur.reset()
        cur = self.conn.cursor(buffered=True)
        self.cur.execute("SELECT `act_id`, `client_id`, `date_create`, `status`, `file_name`, `file_name_edo`, `ms_demand` FROM `acts` WHERE `date_create` > CURDATE()")
        raw_list = self.cur.fetchall()
        # proxy.extend(raw_list)
        # except:
        #     return proxy
        return raw_list

    def insert_act(self, act_id: int, client_id: str):
        try:
            self.cur.execute(
                f"INSERT INTO `acts` (`act_id`, `client_id`, `status`, `file_name`, `file_name_edo`, `ms_demand`) VALUES (%s, %s, 'wait', '', '', 2)",
                (act_id, client_id))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert act table acts error')
            print(e)
            return False
        return True

    def get_wait_acts(self):
        try:
            self.cur.execute("SELECT `act_id`, `client_id`, `date_create`, `date_update`, `file_name` FROM `acts` WHERE `status` = 'wait'")
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_acts_today(self):
        try:
            self.cur.execute("SELECT `act_id`, `client_id`, `date_create`, `date_update`, `file_name` FROM `acts` WHERE `date_create` > CURRENT_DATE()")
            raw_list = self.cur.fetchall()
        except:
            return []
        print('get_acts_today', raw_list)
        return raw_list

    def get_all_acts(self):
        try:
            self.cur.execute("SELECT `act_id`, `client_id`, `date_create`, `date_update` FROM `acts`")
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def update_act(self, act_id: int, file_name: str, file_name_edo: str, status='ready'):
        try:
            self.cur.execute(
                f"UPDATE `acts` SET `status` = %s, `file_name` = %s, `file_name_edo` = %s WHERE `act_id` = %s",
                (status, file_name, file_name_edo, act_id))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL insert file_name acts error')
            logging.warning(e)
            return False
        return True

    def update_act_demand(self, act_id: int, ms_demand: int):
        # ACT demand_ms: 1 - отгружен, 2 - не отгружен, 0 - архив
        try:
            self.cur.execute(
                f"UPDATE `acts` SET `ms_demand` = %s WHERE `act_id` = %s",
                (ms_demand, act_id))
            self.conn.commit()
        except Exception as e:
            logging.warning(f'MySQL updane ms_demand act error')
            logging.warning(e)
            return False
        return True

    def get_orders_stat(self, client_id, period=OZON_ORDERS_OLD_DAYS):
        try:
            self.cur.execute("SELECT `status` FROM `orders` WHERE `client_id` = %s AND date > CURDATE() - INTERVAL %s DAY", (client_id, period))
            raw_list = self.cur.fetchall()
        except:
            return []
        return raw_list

    def get_seller_id_today(self):
        # try:
        self.cur.execute("SELECT `client_id` FROM `orders` WHERE shipment_date > CURDATE()")
        raw_list = self.cur.fetchall()
        # except:
        #     return []
        print('get_seller_id_today', raw_list)
        return raw_list

    def get_orders_stat_today(self):
        try:
            self.cur.execute("SELECT * FROM `orders` WHERE shipment_date > CURDATE()")
            raw_list = self.cur.fetchall()
        except:
            return []
        print('get_orders_stat_today', raw_list)
        return raw_list


    def close(self):
        self.conn.close()
        self.cur.close()
        logging.info('MySQL cursor closed')
