import schedule
from test_data import refresh_access
from maintenance import read_gmotors_link, read_eurozapchastspb_link
import time

schedule.every(720).minutes.do(read_eurozapchastspb_link)
schedule.every(720).minutes.do(read_gmotors_link)
schedule.every(84000).seconds.do(refresh_access)

while True:
    schedule.run_pending()
    time.sleep(1)
