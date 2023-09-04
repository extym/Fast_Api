from datetime import datetime
import requests
import utils
import time
from utils import cur2, price_product, logg
from config import mCur, mSum, mTimeout, mCommis, mProfit, API_key, API_secret, mCount
from binance import Binance
import traceback
import sys


def cur_filter(symbol, filter_type):
    print('cur_filter', symbol, filter_type)
    for ex_inf in exchangeInfo["symbols"]:
        if ex_inf['symbol'] == symbol:
            for ex_filter in ex_inf['filters']:
                if ex_filter['filterType'] == filter_type:
                    return ex_filter
        return False


def order(symbol, quantity, price, side):
    ex_inf_q = cur_filter(symbol, 'LOT_SIZE')
    ex_inf_p = cur_filter(symbol, 'PRICE_FILTER')
    ex_inf_n = cur_filter(symbol, "MIN_NOTIONAL")

    msg = str(ex_inf_n)
    logger.info('<ORDER1>: ' + msg)
    print(msg)
    if float(ex_inf_q['stepSize']) * 100000000 % 100000000 != 0:
        str_q = str('{0:.8f}'.format(quantity))
    else:
        str_q = str('{0:0}'.format(quantity))
    if float(ex_inf_p['tickSize']) * 100000000 % 10000000 != 0:
        str_p = str('{0:.8f}'.format(price))
    elif float(ex_inf_p['tickSize']) * 100000000 % 100000000 != 0:
        str_p = str('{0:.1f}'.format(price))
    else:
        str_p = str('{0:0}'.format(price))
    msg = 'step_size_q = ' + str(ex_inf_q['stepSize']) + ' step_size_p = ' + str(ex_inf_p['tickSize']) + ' symbol = ' + str(symbol) + ' quantity = ' + str(str_q) + ' price = ' + str(str_p) + ' side = ' + str(side)
    logger.info('<ORDER2>: ' + msg)
    print(msg)
    return bot.createOrder(
        symbol=symbol,
        recvWindow=5000,
        side=side,
        type='LIMIT',
        timeInForce='GTC',
        quantity=str_q,
        price=str_p
    )


def order_inf(orig_client_order_id, symbol):
    return bot.orderInfo(
        origClientOrderId=orig_client_order_id,
        symbol=symbol
    )


def check_order(response, symbol):
    if order_inf(response["clientOrderId"], symbol)['status'] == 'FILLED':
        msg = 'ордер закрыт'
        logger.info('<ORDER3>: ' + msg)
        print(msg)
        return False
    else:
        msg = 'Ждем закрытия ордера'
        logger.info('<ORDER4>: ' + msg)
        print(msg)
        return True


def circle(symbol1, symbol2, symbol3, price1, price2, price3):
    step_q1 = float(cur_filter(symbol1, 'LOT_SIZE')['stepSize'])
    step_p1 = float(cur_filter(symbol1, 'PRICE_FILTER')['tickSize'])
    step_q2 = float(cur_filter(symbol2, 'LOT_SIZE')['stepSize'])
    step_p2 = float(cur_filter(symbol2, 'PRICE_FILTER')['tickSize'])
    step_q3 = float(cur_filter(symbol3, 'LOT_SIZE')['stepSize'])
    step_p3 = float(cur_filter(symbol3, 'PRICE_FILTER')['tickSize'])
    # real_quantity2 = 0
    # real_quantity3 = 0
    if not price1[1]:
        side = 'BUY'
        quantity = utils.get_quantity(mSum, price1[0])
        quantity2 = quantity
        quantity2 = quantity2 - quantity2 * mCommis
    else:
        side = 'SELL'
        quantity = mSum
        quantity2 = mSum * price1[0]
        quantity2 = quantity2 - quantity2 * mCommis
    real_quantity2 = quantity2
    quantity = utils.cor_step(step_q1, quantity)
    price1[0] = utils.cor_step(step_p1, price1[0])
    print('Данные ')
    msg = 'quantity= ' + str(quantity) + ' price= ' + str(price1) + ' symbol= ' + str(symbol1)
    logger.info('<ORDER5>: ' + msg)
    print(msg)
    response1 = order(symbol1, quantity, price1[0], side)
    msg ='открываю первый ордер'
    logger.info('<ORDER6>: ' + msg)
    print(msg)
    while check_order(response1, symbol1):
        time.sleep(2)
    if not price2[1]:
        side = 'BUY'
        quantity2 = utils.get_quantity(quantity2, price2[0])
        quantity3 = quantity2
        quantity2 = utils.cor_quantity(real_quantity2, quantity2 * price2[0], step_q2)
        quantity2 = utils.cor_step(step_q2, quantity2)
        price2[0] = utils.cor_step(step_p2, price2[0])
        quantity3 = quantity3 - quantity3 * mCommis
    else:
        side = 'SELL'
        quantity3 = quantity2 * price2[0]
        quantity2 = utils.cor_step(step_q2, quantity2)
        price2[0] = utils.cor_step(step_p2, price2[0])
        quantity3 = quantity3 - quantity3 * mCommis
    if quantity2 > real_quantity2:
        msg = 'ERROR: qu = ' + str(quantity2) + ' real = ' + str(real_quantity2)
        logger.info('<ORDER7>: ' + msg)
        print(msg)
    real_quantity3 = quantity3
    msg = 'Данные'
    logger.info('<ORDER>: ' + msg)
    print(msg)
    msg = 'quantity=' + str(quantity2) + 'price=' + str(price2) + 'symbol=' + str(symbol2)
    logger.info('<ORDER8>: ' + msg)
    print(msg)
    response2 = order(symbol2, quantity2, price2[0], side)
    msg = 'открываю второй ордер'
    logger.info('<ORDER9>: ' + msg)
    print(msg, response2)
    while check_order(response2, symbol2):
        time.sleep(2)
    if not price3[1]:
        side = 'BUY'
        quantity3 = utils.get_quantity(quantity3, price3[0])
        quantity3 = utils.cor_quantity(real_quantity3, quantity3 * price3[0], step_q3)
        quantity3 = utils.cor_step(step_q3, quantity3)
    else:
        side = 'SELL'
        quantity3 = utils.cor_step(step_q3, quantity3)
    msg = 'quantity=' + str(quantity3) + 'price=' + str(price3) + 'symbol=' + str(symbol3)
    logger.info('<ORDER10>: ' + msg)
    print(msg)
    quantity3 = utils.cor_step(step_q3, quantity3)
    price3[0] = utils.cor_step(step_p3, price3[0])
    if quantity3 > real_quantity3:
        msg = 'ERROR: qu = ' + str(quantity3) + ' real = ' + str(real_quantity3)
        logger.info('<ORDER12>: ' + msg)
        print(msg)
    response3 = order(symbol3, quantity3, price3[0], side)
    msg = 'открываю третий ордер'
    logger.info('<ORDER13>: ' + msg)
    print(msg)
    while check_order(response3, symbol3):
        time.sleep(2)


def get_cor_price(symbol, cur):
    return correct_price(get_price(symbol), cur)


def get_prices(symbols):
    return bot.tickerBookTicker(  # bot.tickerPrice(
        symbols=str(symbols).replace('\'', '\"').replace(' ', '')
    )


def get_price(symbol):
    return bot.tickerBookTicker(  # bot.tickerPrice(
        symbol=str(symbol)
    )


def correct_price(bookTicker, cur):
    if utils.left_pos_symbol(bookTicker['symbol'], cur):
        price = float(bookTicker['bidPrice'])
        return [price, True]
    else:
        price = float(bookTicker['askPrice'])
        return [price, False]


def get_main_symbols():
    data = []
    for dat in response.json()['data']:
        if dat['q'] == mCur or dat['b'] == mCur:
            data.append(dat['s'])
    unsorted_list = bot.ticker24hr(
        symbols=str(data).replace('\'', '\"').replace(' ', '')
    )
    sorted_list = utils.quicksort(unsorted_list)
    return sorted_list


if __name__ == '__main__':
    try:
        log = logg()
        logger = log.loging_init()
        while True:
            circle_complete = False
            start_time = datetime.now()
            bot = Binance(
                API_KEY=API_key,
                API_SECRET=API_secret
            )
            if bot.ping() == {}:
                logger.info('<MAIN>: Подключение API успешно произведено')
                print('Подключение API успешно произведено')
            msg = 'Время сервера: ' + str(utils.epoch_time_to_str(float(bot.time()['serverTime']) / 1000))
            logger.info('<MAIN>: ' + msg)
            print(msg)
            exchangeInfo = bot.exchangeInfo()
            headers = {}
            response = requests.request(method='GET',
                                        url='https://binance.com/exchange-api/v2/public/asset-service/product/get-products',
                                        data="",
                                        headers=headers
                                        )
            allSymbols = response.json()['data']
            sorted_data = get_main_symbols()
            part_sort_data = sorted_data[0:mCount]
            spar_names_two = []
            spar_name_first = []
            for i in part_sort_data:
                par = []
                for a in allSymbols:
                    if (a['b'] == cur2(i['symbol'], mCur) and a['q'] != 'USDT') or (
                            a['q'] == cur2(i['symbol'], mCur) and a['b'] != 'USDT'):
                        par.append(a['s'])
                if len(par) != 0:
                    spar_name_first.append(i['symbol'])
                    spar_names_two.append(par)
            temp_first_price = get_prices(spar_name_first)
            spar_first_price = utils.list_to_list(spar_name_first, temp_first_price)
            for ind in range(len(spar_name_first)):
                spar_price = get_prices(spar_names_two[ind])
                for spar_two_price_i in spar_price:
                    temp_two_cur = cur2(spar_name_first[ind], mCur)
                    temp_three_cur = cur2(spar_two_price_i['symbol'], cur2(spar_name_first[ind], mCur))
                    d_price = correct_price(spar_first_price[ind], mCur)
                    p_price = correct_price(spar_two_price_i, temp_two_cur)
                    for c in spar_first_price:
                        if c['symbol'] == temp_three_cur + mCur or c['symbol'] == mCur + temp_three_cur:
                            t_price = correct_price(c, temp_three_cur)
                            h = price_product(d_price, p_price, t_price)
                            if h > mProfit:
                                msg = 'Найдена связка: '
                                logger.info('<MAIN>: ' + msg)
                                print(msg)
                                start_time3 = datetime.now()
                                msg = str(mCur + temp_two_cur) + '-' + str(d_price)
                                logger.info('<MAIN>: ' + msg)
                                print(msg)
                                msg = str(temp_two_cur + temp_three_cur) + '-' + str(p_price)
                                logger.info('<MAIN>: ' + msg)
                                print(msg)
                                msg = str(c['symbol']) + '-' + str(t_price)
                                logger.info('<MAIN>: ' + msg)
                                print(msg)
                                msg = 'h =' + str(h)
                                logger.info('<MAIN>: ' + msg)
                                print(msg)
                                trig = True
                                trig_i = 0
                                while trig:
                                    price_one = get_cor_price(spar_name_first[ind], mCur)
                                    price_two = get_cor_price(spar_two_price_i['symbol'], temp_two_cur)
                                    price_three = get_cor_price(c['symbol'], temp_three_cur)
                                    h2 = price_product(price_one, price_two, price_three)
                                    if h2 <= mProfit:
                                        trig = False
                                        msg = 'Связка закрыта. Связка была открыта:' + str(datetime.now() - start_time3)
                                        logger.info('<MAIN>: ' + msg)
                                        print(msg)
                                        msg = 'прибль закрытия:' + str(h2)
                                        logger.info('<MAIN>: ' + msg)
                                        print(msg)
                                    elif trig_i >= mTimeout:
                                        trig = False
                                        g = [str(spar_name_first[ind]), str(spar_two_price_i['symbol']), str(c['symbol'])]
                                        for r in bot.ticker24hr(
                                                symbols=str(g).replace('\'', '\"').replace(' ', '')
                                        ):
                                            msg = str(r['symbol']) + ' quoteVolume = ' + str(r['quoteVolume']) + ' price = ' + str(r["lastPrice"])
                                            logger.info('<MAIN>: ' + msg)
                                            print(msg)
                                            if float(r['quoteVolume']) > 30:
                                                msg = 'Связка прочная.'
                                                logger.info('<MAIN>: ' + msg)
                                                print(msg)
                                                msg = 'Прибль закрытия:' + str(h2)
                                                logger.info('<MAIN>: ' + msg)
                                                print(msg)
                                                circle(str(spar_name_first[ind]),
                                                       str(spar_two_price_i['symbol']),
                                                       c['symbol'], price_one, price_two, price_three)
                                                msg = 'связка завершена'
                                                logger.info('<MAIN>: ' + msg)
                                                print(msg)
                                                circle_complete = True
                                                break
                                    trig_i = trig_i + 1
                                    if circle_complete:
                                        break
                        if circle_complete:
                            break
                    if circle_complete:
                        break
                if circle_complete:
                    break

            msg = '___________ПРОГОН ЗАВЕРШЕН. время выполнения: ' + str(datetime.now() - start_time)
            logger.info('<MAIN>: ' + msg)
            print(msg)
    except:
        tb = sys.exc_info()[2]
        tbinfo = ''.join(traceback.format_tb(tb))
        er = sys.exc_info()
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(er)
        print(pymsg)
        #logger.info('<MAIN>: ' + pymsg)
        logger.exception('<MAIN>')
        a = input('Ошибка. Нажмите Enter чтобы остановить программу.')