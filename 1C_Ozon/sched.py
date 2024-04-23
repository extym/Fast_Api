import asyncio

import schedule
import time
from y_data import create_fbs, create_expresso, create_dbs
from o_data import o_create
from ozon import send_stocks_on
from wildberry import send_stocks_wb
from leroy import send_stocks_lm, get_new_orders_lm, send_price_lm,  make_log
from sper import send_stocks_sb
from wildberry import processing_orders_wb
import datetime
import os

def job_lm():
    asyncio.run(get_new_orders_lm())

def job_wb():
    asyncio.run(processing_orders_wb())

# def make_log():
#     # PATH = '/var/www/html/stm/'
#     today = str(datetime.datetime.today()).replace(' ', '_')[:-7]
#     try:
#         os.system(f'cp /var/www/html/stm/test_json.json /var/www/html/stm/test_json_{today}.json')
#         print("ALL_RIDE_make_log_json")
#     except:
#         print("FACK_UP_make_log_json")


# schedule.every(151).seconds.do(job)

schedule.every(10).minutes.do(job_lm)
schedule.every(10).minutes.do(job_wb)
schedule.every(600).seconds.do(send_stocks_lm)
schedule.every(10).minutes.do(send_price_lm)
schedule.every(600).seconds.do(send_stocks_on)
schedule.every(600).seconds.do(send_stocks_sb)
schedule.every(600).seconds.do(send_stocks_wb)

# schedule.every(2592000).seconds.do(send_get_token)
# schedule.every(2592000).seconds.do(get_jwt_token_orders)

schedule.every(360).minutes.do(make_log)
# schedule.every(1798).seconds.do(create_expresso)
# schedule.every(1797).seconds.do(create_fbs)
# schedule.every(1771).seconds.do(o_create)

# schedule.every(300).seconds.do(five)
# schedule.every(600).seconds.do(ten)
# schedule.every(10).minutes.do(tt)

#
while True:
    schedule.run_pending()
    time.sleep(1)
