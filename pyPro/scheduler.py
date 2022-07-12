import schedule
import time
from main import get_data

# def job():
#     print("I'm working...")

schedule.every(2).minutes.do(get_data)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(5)