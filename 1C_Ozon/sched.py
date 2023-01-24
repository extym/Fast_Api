import schedule
import time
from y_data import create
from o_data import o_create



# schedule.every(151).seconds.do(job)
schedule.every(1799).seconds.do(create)
schedule.every(1771).seconds.do(o_create)

while True:
    schedule.run_pending()
    time.sleep(1)
