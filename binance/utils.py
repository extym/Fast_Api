import math
import random
import logging.config
import logging
import logging.handlers
from config import mSum, mCommis


def cor_step(step, qp):
    if float(step) * 100000000 % 100000000 != 0:
        return float(step) * math.floor(float(qp) / float(step))
    else:
        return float(step) * (float(qp) // float(step))


def cor_quantity(r_qu, qu, step):
    res = qu
    while res > r_qu:
        if res > r_qu:
            res -= step
    return res


def get_quantity(quantity, price):
    price1 = int(price * 100000000)
    quantity1 = int(quantity * 10000000000000000)
    return (quantity1 // price1) / 100000000


def quicksort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
        s_nums = []
        m_nums = []
        e_nums = []
        for n in nums:
            if float(n['quoteVolume']) > float(q['quoteVolume']):
                s_nums.append(n)
            elif float(n['quoteVolume']) < float(q['quoteVolume']):
                m_nums.append(n)
            else:
                e_nums.append(n)
        return quicksort(s_nums) + e_nums + quicksort(m_nums)


def epoch_time_to_str(timestamp, *, round_=6):
    import time
    s = time.strftime('%Y.%m.%d %H:%M:%S', time.gmtime(timestamp))
    s += ('%.9f' % round(timestamp - int(timestamp), round_))[1:].rstrip('0').rstrip('.')
    s += ' UTC'
    return s


def left_pos_symbol2(symbol1, symbol2, cur):
    return left_pos_symbol(symbol2, cur2(symbol1, cur))


def left_pos_symbol(symbol, cur):
    if cur + cur2(symbol, cur) == symbol:
        return True
    elif cur + cur2(symbol, cur) != symbol:
        return False
    else:
        print('Error, uncorrected symbol')
        return 'Error, uncorrected symbol'


def cur2(symbol, cur):
    return symbol.replace(cur, '')


def list_to_list(symbol, bookTicker):
    fin_list = []
    for l1 in symbol:
        for l2 in bookTicker:
            if l1 == l2['symbol']:
                fin_list.append(l2)
    return fin_list


def price_product(price1, price2, price3):
    t_price1 = price1[0]
    t_price2 = price2[0]
    t_price3 = price3[0]
    if not price1[1]:
        t_price1 = 1 / t_price1
    if not price2[1]:
        t_price2 = 1 / t_price2
    if not price3[1]:
        t_price3 = 1 / t_price3
    t_quantity1 = t_price1 * mSum
    t_quantity1 = t_quantity1 - t_quantity1 * mCommis
    t_quantity2 = t_price2 * t_quantity1
    t_quantity2 = t_quantity2 - t_quantity2 * mCommis
    t_quantity3 = t_price3 * t_quantity2
    t_quantity3 = t_quantity3 - t_quantity3 * mCommis
    return t_quantity3 - mSum


class logg():
    def __init__(self):
        self.LOGGING_CONFIG = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'default_formatter': {
                    'format': '[%(levelname)s:%(asctime)s] %(message)s'
                }
            },
            'handlers': {
                'file_handler': {
                    'class': 'logging.FileHandler',
                    'filename': 'binance.log',
                    'formatter': 'default_formatter'
                }
            },
            'loggers': {
                'my_logger': {
                    'handlers': ['file_handler'],
                    'level': 'DEBUG',
                    'propagate': True
                }
            }
        }
    def loging_init(self):
        logging.config.dictConfig(self.LOGGING_CONFIG)
        logger = logging.getLogger('my_logger')
        return logger