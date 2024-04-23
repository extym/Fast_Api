import time

import schedule
from cron_order import start_orders

schedule.every(10).minutes.do(start_orders)

while True:
    schedule.run_pending()
    time.sleep(1)