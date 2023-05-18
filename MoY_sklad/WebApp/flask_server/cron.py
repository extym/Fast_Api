"""
Cron Jobs
"""
import threading
import os
import sys
import logging

import ms
import ozon
from database import MsDatabase

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, DB_DICTS, PUBLIC_DIR, LOG_FILE

if __name__ == '__main__':
    #################### TESTS ######################
    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    # header = ozon.get_header("7660a38f-a39b-4a9a-99a4-32c5ffb44edf", "118614")
    # res = ozon.get_products_dict(header)
    # print(res)
    # print(len(res))
    # for key in res:
    #     print(ozon.get_product_dict(key, header))
    #     break
    # db.close()
    # res = ms.get_small_service_list()
    # print(res)
    # sys.exit(0)
    #################################################
    # logging.basicConfig(filename=os.path.join(PUBLIC_DIR, LOG_FILE),
    logging.basicConfig(filename=os.path.join(LOG_FILE),
                        format='[%(asctime)s] [%(levelname)s] => %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logging.info('=' * 50)
    logging.info('CRON DICTS started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)

    ############## MS organizations, Contragents ############
    for entity in DB_DICTS:
        res = ms.get_entity_id_name_meta(entity)
        # print(len(res))
        for elem in res:
            db.insert_update_dict(entity, elem[0], elem[1], elem[2])

    ###################### MS States #######################
    res = ms.get_states_id_name_meta()
    # print(len(res))
    logging.info(f"States dict {len(res)}")
    for elem in res:
        db.insert_update_dict('states', elem[0], elem[1], elem[2])

    ###################### MS Prices #######################
    res = ms.get_prices_id_name_meta()
    # print(len(res))
    logging.info(f"Prices dict {len(res)}")
    for elem in res:
        db.insert_update_dict('prices', elem[0], elem[1], elem[2])

    ################### Ozon products ######################
    sellers = db.get_active_sellers_id_token()
    # print(sellers)
    for seller in sellers:
        header = ozon.get_header(seller[1], seller[0])
        res = ozon.get_products_dict(header)
        # print(len(res))
        logging.info(len(res))
        for key in res:
            product = ozon.get_product_dict(key, header)
            db.insert_update_ozon_product(seller[0], product)

    ################ MS products ####################
    res = ms.get_small_products_list()
    for product in res:
        db.insert_update_ms_product(product)
    # print(res)
    # print(len(res))
    logging.info(len(res))

    db.close()

    sys.exit(0)

    
