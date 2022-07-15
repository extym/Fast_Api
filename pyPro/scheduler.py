import schedule
import time


def job():
    print('And now print')

from main import get_data, print_data

def job_two():
    print('And now print' + print_data())

schedule.every(40).seconds.do(job)
schedule.every(60).seconds.do(job_two)

schedule.every(20).seconds.do(print_data)
schedule.every(180).seconds.do(get_data)

while True:
    schedule.run_pending()
    time.sleep(1)