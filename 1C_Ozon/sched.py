import schedule
import time
from y_data import create_fbs, create_expresso, create_dbs
from o_data import o_create



# schedule.every(151).seconds.do(job)
schedule.every(1799).seconds.do(create_dbs)
schedule.every(1798).seconds.do(create_expresso)
schedule.every(1797).seconds.do(create_fbs)
schedule.every(1771).seconds.do(o_create)

while True:
    schedule.run_pending()
    time.sleep(1)
