import schedule
import time
import create_file as ym
import sber_data as sb

def job():
    ym.create_ym_xml(stocks_is_null=False, without_db=True)
    sb.create_sber_xml(stocks_is_null=True, without_db=True)

schedule.every(60).minutes.do(job)
schedule.every(4).hour.do(ym.create_ym_xml)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)