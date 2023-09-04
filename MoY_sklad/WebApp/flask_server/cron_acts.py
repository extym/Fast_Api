import shutil
import threading
import datetime
import os
import sys
import logging
from pathlib import Path

from pypdf import PdfMerger
import ozon
import ms
import time
from database import MsDatabase

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, PUBLIC_DIR, ACTS_LOG_FILE, ACT_DIR, LOCAL_MODE, \
    MS_FIELD_SOBRAN_BOOL

if __name__ == '__main__':
    ###################################################################
    # header = ozon.get_header('442a5775-7c00-450f-8946-0cfb286cff79', "139714")
    # file_name_edo = ozon.get_edo_act_by_code(4963297, PUBLIC_DIR + ACT_DIR, header)
    # print(file_name_edo)
    # exit(0)

    # db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    # wait_acts = db.get_all_acts()
    # for wait_act in wait_acts:
    #     seller_id = wait_act[1]
    #     act_id = wait_act[0]
    #     seller = db.get_seller(seller_id)[0]
    #     header = ozon.get_header(seller[4], seller_id)
    #     file_name1 = ozon.get_act_by_code_v2(act_id, PUBLIC_DIR + ACT_DIR, header)
    #     file_name2 = ozon.get_edo_act_by_code(act_id, PUBLIC_DIR + ACT_DIR, header)
    #     print(file_name1, file_name2)
    # exit(0)
    ###################################################################
    # logging.basicConfig(filename=os.path.join(PUBLIC_DIR, ACTS_LOG_FILE),
    #                     format='[%(asctime)s] [%(levelname)s] => %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    # logging.info('=' * 50)
    # logging.info('Cron orders Started')

    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)

    wait_acts = db.get_wait_acts()
    print('wait_acts', wait_acts)
    logging.info(f'{len(wait_acts)} waiting acts')
    for wait_act in wait_acts:
        seller_id = wait_act[1]
        act_id = wait_act[0]
        exist_file = wait_act[4]
        seller = db.get_seller(seller_id)[0]
        header = ozon.get_header(seller[4], seller_id)

        # file_name = ozon.get_act_by_code_v2(act_id, PUBLIC_DIR + ACT_DIR, header)
        file_name = ozon.get_digital_act_by_code(act_id, PUBLIC_DIR + ACT_DIR, header)
        file_name_edo = ozon.get_edo_act_by_code(act_id, PUBLIC_DIR + ACT_DIR, header)
        print('file_name_edo', file_name_edo)
        # if file_name_edo is None:
        #     file_name_edo = ''
            # time.sleep(2 * 60)
            # db.reconnect()
            # file_name_edo = ozon.get_edo_act_by_code(act_id, PUBLIC_DIR + ACT_DIR, header)
            # if file_name_edo is None:
            #     file_name_edo = ''
        if file_name or file_name_edo:
            status = 'ready'
            if not exist_file and not file_name_edo:
                status = 'wait'
                file_name_edo = ''
            if not db.update_act(act_id, file_name, file_name_edo, status):
                logging.warning(f"Act {act_id}, file {file_name}, file_name_edo {file_name_edo} - error writing in DB")
            else:
                logging.info(f"Act {act_id}, file {file_name}, file_name_edo {file_name_edo} - ready")
        else:
            logging.info(f"Act order {act_id} doesn't ready")

        # report_file = ozon.get_act_by_code(act_id, header)
        # if report_file:
        #     file_name = ozon.get_file(report_file, PUBLIC_DIR + ACT_DIR, header)
        #     print(file_name)
        #     if file_name:
        #         if not db.update_act(act_id, file_name):
        #             logging.warning(f"Act {act_id}, file {file_name} - error writing in DB")
        #         else:
        #             logging.info(f"Act {act_id}, file {file_name} - ready")
        # else:
        #     logging.info(f"Act order {act_id} doesn't ready")


    ##############################################################################################
        ######################################################/root/WebApp/public_html/labels_not_assembled
        ############## Несобранные заказы за сегодня #########
        ######################################################

    merger = PdfMerger()

    dt_now = datetime.datetime.now()
    arr_pdf = []
    # shipments_today = db.get_orders_stat_today()
    rows_act = db.get_acts_today()

    if LOCAL_MODE:
    #     dt_now = datetime.datetime(2022, 11, 14)
    #     arr_pdf = ['03975825-0093-2.pdf', '04995274-0037-1.pdf', '07542624-0051-1.pdf']
    #
    # else:
        for order in rows_act:
            pdf = order[0]
            arr_pdf.append(f'{pdf}.pdf')
            #time.sleep(2)
            print('arr_pdf', arr_pdf)

    shutil.rmtree('/root/WebApp/public_html/acts_not_assembled_day', ignore_errors=True)

    time.sleep(2)

    try:
        p = Path(PUBLIC_DIR + '/acts_not_assembled_day')
        p.mkdir(parents=True)
    except:
        pass

    for pdf in arr_pdf:
        try:
            shutil.copy(f'{PUBLIC_DIR}/acts/{pdf}',
                        f'{PUBLIC_DIR}/acts_not_assembled_day/{pdf}')
            print("Copy")
        except Exception as ex:
            print(str(ex))
            pass

    # files = os.listdir("/root/WebApp/public_html/acts_not_assembled_day")
    files = os.listdir(PUBLIC_DIR + "/acts_not_assembled_day")

    try:
        # os.remove("/root/WebApp/public_html/acts_not_assembled_day/all_acts_day.pdf")
        os.remove(PUBLIC_DIR + "/acts_not_assembled_day/all_acts_day.pdf")
    except:
        pass

    for filename in files:

        try:
            merger.append(
                # fileobj=open(os.path.join("/root/WebApp/public_html/acts_not_assembled_day", filename), 'rb'))
                fileobj=open(os.path.join(PUBLIC_DIR + "/acts_not_assembled_day", filename), 'rb'))
        except Exception as ex:
            pass

    time.sleep(2)

    try:
        merger.write(
            # open(os.path.join("/root/WebApp/public_html/acts_not_assembled_day", 'all_acts_day.pdf'), 'wb'))
            open(os.path.join(PUBLIC_DIR + "/acts_not_assembled_day", 'all_acts_day.pdf'), 'wb'))
    except Exception as ex:
        pass

    time.sleep(2)

    print("За сегодня acts")

    merger.close()


    db.close()
    sys.exit(0)
