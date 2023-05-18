# -- coding: utf-8 --
import os, glob
import sys
from pathlib import Path
import shutil
from pypdf import PdfMerger
import datetime
import time

import ms
import ozon
from database import MsDatabase

from settings import LOG_FILE, PUBLIC_DIR, MYSQL_HOST, MYSQL_USER, MYSQL_PASW, MYSQL_DATABASE, LOGGING, \
    LOGIN, PASSW, TEST_MODE, OZON_COMMENT_FIELDS, OZON_DATA_FIELDS, OZON_TYPES, MS_DEFAULT_PRICE, LABEL_DIR, URL, \
    ACT_DIR, MS_FIELD_SOBRAN_BOOL, MS_DEMAND_STATUS_PAYED, MS_DEMAND_STATUS_NOT_PAYED, MS_ORDER_STATUS_NOT_PAYED, \
    MS_MINUS_STATUS, LOCAL_MODE, OZON_HEADERS

if __name__ == '__main__':
    
    ######################################################
    ############## Все несобранные заказы ################
    ######################################################
    db = MsDatabase(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASW, database=MYSQL_DATABASE)
    
    rows = db.get_all_orders()
    
    if rows == False:
        db.close()
        sys.exit(0)
    
    else:
        arr_pdf = []
        if LOCAL_MODE:
            arr_pdf = ['03975825-0093-2.pdf', '04995274-0037-1.pdf', '07542624-0051-1.pdf']
            print("Local Mode")
        else:
            dt = datetime.datetime.now()
            for i in range(len(rows)):
                order_href = rows[i][13]
                if rows[i][1].year == dt.year and rows[i][15] == 1 and rows[i][18] != 3 and rows[i][4] != 'cancelled':
                    order_dict = ms.get_order_params_and_attributes(order_href, ['name', 'demands', 'payments', 'sum'], [MS_FIELD_SOBRAN_BOOL])
                    #####################################################
                    #r = ozon.is_order_cansel(rows[i][2], OZON_HEADERS)
                    if order_dict[MS_FIELD_SOBRAN_BOOL] == None or order_dict[MS_FIELD_SOBRAN_BOOL] == False:
                        pdf = rows[i][2]
                        #print(str(order_dict) + ' Выгрузилось')
                        arr_pdf.append(f'{pdf}.pdf')
                        #print(f"Not assembled {pdf}.pdf")
                    time.sleep(1)
            #print(arr_pdf)
                
        shutil.rmtree(PUBLIC_DIR + '/labels_not_assembled', ignore_errors=True)
        
        print('Deleted all')
        time.sleep(2)
        
        try:
            p = Path(PUBLIC_DIR + 'labels_not_assembled')
            p.mkdir(parents=True)
        except Exception as ex:
            print(str(ex))
        
        for pdf in arr_pdf:
            try:
                shutil.copy(f'{PUBLIC_DIR}/labels/{pdf}',f'{PUBLIC_DIR}labels_not_assembled/{pdf}')
                #print("Copy")
            except Exception as ex:
                print(str(ex))

        time.sleep(2)
        
        files = os.listdir(PUBLIC_DIR + "labels_not_assembled")
        #print(files)
        
        try:
            os.remove(PUBLIC_DIR + "labels_not_assembled/all_labels.pdf")
        except:
            pass
        
        merger = PdfMerger()
        
        for filename in files:
            try:
                merger.append(fileobj=open(os.path.join(PUBLIC_DIR + "/labels_not_assembled", filename),'rb'))
                #print("Join")
            except Exception as ex:
                pass
                #print(str(ex))

        time.sleep(2)

        try:
            merger.write(open(os.path.join(PUBLIC_DIR + "labels_not_assembled",'all_labels.pdf'), 'wb'))
        except:
            pass
        
        print("Отработали все заказы")
        
        merger.close()
        
        ######################################################/root/WebApp/public_html/labels_not_assembled
        ############## Несобранные заказы за сегодня #########
        ######################################################
        
        merger = PdfMerger()
        
        dt_now = datetime.datetime.now()
        
        arr_pdf = []
        
        if LOCAL_MODE:
            dt_now = datetime.datetime(2022, 11, 14)
            arr_pdf = ['03975825-0093-2.pdf', '04995274-0037-1.pdf', '07542624-0051-1.pdf']
        else:
            for i in range(len(rows)):
                order_href = rows[i][13]
                ship_date = str(rows[i][5])
                ship_date_list = ship_date.split('T')
                dt = ship_date_list[0].split('-')
                if int(dt[0]) == dt_now.year and int(dt[1]) == dt_now.month and int(dt[2]) == dt_now.day and rows[i][15] == 1 and rows[i][18] != 3 and rows[i][4] != 'cancelled':
                    order_dict = ms.get_order_params_and_attributes(order_href, ['name', 'demands', 'payments', 'sum'], [MS_FIELD_SOBRAN_BOOL])
                    if order_dict[MS_FIELD_SOBRAN_BOOL] == None or order_dict[MS_FIELD_SOBRAN_BOOL] == False:
                        pdf = rows[i][2]
                        arr_pdf.append(f'{pdf}.pdf')
                        #print(ship_date)
                        #print(f"Not assembled {pdf}.pdf")
                    time.sleep(2)
                    
        shutil.rmtree(PUBLIC_DIR + 'labels_not_assembled_day', ignore_errors=True)
            
        time.sleep(2)
        
        try:
            p = Path(PUBLIC_DIR + 'labels_not_assembled_day')
            p.mkdir(parents=True)
        except:
            pass
        
        for pdf in arr_pdf:
            try:
                shutil.copy(f'{PUBLIC_DIR}labels/{pdf}',f'{PUBLIC_DIR}labels_not_assembled_day/{pdf}')
                #print("Copy")
            except Exception as ex:
                #print(str(ex))
                pass
        
        
        files = os.listdir(PUBLIC_DIR + "labels_not_assembled_day")
        
        try:
            os.remove(PUBLIC_DIR + "labels_not_assembled_day/all_labels_day.pdf")
        except:
            pass
            
        for filename in files:
            try:
                merger.append(fileobj=open(os.path.join(PUBLIC_DIR + "labels_not_assembled_day", filename),'rb'))
            except Exception as ex:
                pass
            
        time.sleep(2)
    
        try:
            merger.write(open(os.path.join(PUBLIC_DIR + "labels_not_assembled_day",'all_labels_day.pdf'), 'wb'))
        except Exception as ex:
            pass
        
        time.sleep(2)
        
        print("За сегодня")

    merger.close()
    db.close()
    sys.exit(0)