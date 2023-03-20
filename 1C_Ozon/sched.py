import asyncio

import schedule
import time
from y_data import create_fbs, create_expresso, create_dbs
from o_data import o_create
from ozon import send_stocks_on
from wildberry import send_stocks_wb
from leroy import send_stocks_lm, get_new_orders_lm, send_price_lm
from sper import send_stocks_sb
def job():
    asyncio.run(get_new_orders_lm())

# schedule.every(151).seconds.do(job)
schedule.every(1799).seconds.do(create_dbs)
schedule.every(1798).seconds.do(create_expresso)
schedule.every(1797).seconds.do(create_fbs)
schedule.every(1771).seconds.do(o_create)
schedule.every(600).seconds.do(send_stocks_lm)
schedule.every(10).minutes.do(send_price_lm)
schedule.every(595).seconds.do(send_stocks_on)
schedule.every(590).seconds.do(send_stocks_wb)
schedule.every(585).seconds.do(send_stocks_sb)
schedule.every(10).minutes.do(job)
#
while True:
    schedule.run_pending()
    time.sleep(1)
