import schedule
from avito import  get_avito_token_v2, get_current_balance
from amo import refresh_access_main_amo
from maintenance import read_gmotors_link, read_eurozapchastspb_link
import time

schedule.every(720).minutes.do(read_eurozapchastspb_link)
schedule.every(720).minutes.do(read_gmotors_link)
# schedule.every(720).minutes.do(get_avito_token_v2)
schedule.every(1).day.at("22:28").do(get_avito_token_v2)
schedule.every(1).day.at("10:28").do(get_avito_token_v2)
schedule.every(1).day.at("10:30").do(get_current_balance)
schedule.every(82000).seconds.do(refresh_access_main_amo)


while True:
    schedule.run_pending()
    time.sleep(1)
