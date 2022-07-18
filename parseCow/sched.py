import schedule
import time
from main import send_url

def job():
    print('And now we try send -')


# def job_two():
#     print('And now print' + print_data())

schedule.every(160).seconds.do(job)
schedule.every(180).seconds.do(send_url)
# schedule.every(60).seconds.do(job_two)
#
# schedule.every(20).seconds.do(print_data)


while True:
    schedule.run_pending()
    time.sleep(1)