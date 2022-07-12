import schedule
import time
from main import get_data

# def job():
#     print("I'm working...")

schedule.every(120).seconds.do(get_data)


while True:
    schedule.run_pending()
    time.sleep(1)