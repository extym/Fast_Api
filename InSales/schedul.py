import asyncio
from ocs import create_csv_for_category_from_ocs_v3
import schedule
import time
# from y_data import create_fbs, create_expresso, create_dbs
from logic import create_csv_for_category_from_logic
from netlab import get_netlab_token, create_csv_for_category_from_netlab_v3, create_csv_for_category_from_netlab_v4
from marvel import create_csv_for_category_from_marvel_v2
from treolan import create_csv_for_category_from_treolan
from merlion import create_csv_for_category_from_merlion

# def job_netlab():
#     asyncio.run(create_csv_file_from_netlab_v2())
#
# def job_wb():
#     asyncio.run(processing_orders_wb())

# schedule.every(151).seconds.do(job)
# schedule.every(1799).seconds.do(create_dbs)
# schedule.every(1798).seconds.do(create_expresso)
# schedule.every(1797).seconds.do(create_fbs)
# schedule.every(1771).seconds.do(o_create)
# schedule.every(600).seconds.do(send_stocks_lm)
# schedule.every(10).minutes.do(send_price_lm)
schedule.every(16900).seconds.do(get_netlab_token)
schedule.every(120).minutes.do(create_csv_for_category_from_marvel_v2)
schedule.every(120).minutes.do(create_csv_for_category_from_netlab_v4)
schedule.every(120).minutes.do(create_csv_for_category_from_ocs_v3)
schedule.every(120).minutes.do(create_csv_for_category_from_logic)
schedule.every(120).minutes.do(create_csv_for_category_from_merlion)
schedule.every(120).minutes.do(create_csv_for_category_from_treolan)
# schedule.every(10).minutes.do(job_wb)
# #
while True:
    schedule.run_pending()
    time.sleep(1)
