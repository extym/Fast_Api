import schedule
import time
from main import send_url, get_data, confirm_data, proxy_list


# def job():
#     print('And now try send -')
#     print('save_data - ', save_data())
#     print('get_data - ', get_data())
#     print('check_data - ', check_data())
#     print('send_url - ', send_url())
#     print('proxy_list - ', proxy_list)


# schedule.every(151).seconds.do(job)
schedule.every(251).seconds.do(send_url)

while True:
    schedule.run_pending()
    time.sleep(1)
