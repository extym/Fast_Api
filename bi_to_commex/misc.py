# -*- coding: utf-8 -*-

import ast
import trading_api
from config import *
import datetime
from sys import exc_info
from traceback import extract_tb
import time
import Settings

from talipp.ohlcv import OHLCVFactory
from talipp.indicators import RSI, ParabolicSAR

def get_ohlcv(klines):
    ohlcv = OHLCVFactory.from_matrix2([
        [float(item[1]) for item in klines],
        [float(item[2]) for item in klines],
        [float(item[3]) for item in klines],
        [float(item[4]) for item in klines],
        [float(item[5]) for item in klines]]
    )
    return ohlcv

def get_rsi(period, klines):
    close = [float(item[4]) for item in klines]
    return RSI(period, close)

def getSymbols():
    symbols = ["-"]
    exchangeInfo = trading_api.get_exchange_information()["symbols"]
    for exch in exchangeInfo:
        if "_" not in exch["symbol"]:
            symbols.append(exch["symbol"])

    return symbols

def getExchangeInfo():
    result = {}

    exchangeInfo = trading_api.get_exchange_information()["symbols"]

    for exch in exchangeInfo:
        if exch["status"] == "TRADING":
            for filter in exch["filters"]:

                if filter["filterType"] == "LOT_SIZE":
                    try:
                        minQty = float(filter["minQty"])
                        if "e" not in str(minQty):
                            if minQty < 1:
                                minQty = len(list(str(minQty).split(".")[1]))
                            else:
                                minQty = 0
                        else:
                            minQty = int(str(minQty).split("-")[-1])

                    except:
                        minQty = 0

                elif filter["filterType"] == "PRICE_FILTER":
                    try:
                        minPrice = float(filter["tickSize"])

                        if "e" not in str(minPrice):
                            if minPrice < 1:
                                minPrice = len(list(str(minPrice).split(".")[1]))
                            else:
                                minPrice = 0
                        else:
                            minPrice = int(str(minPrice).split("-")[-1])

                    except:
                        minPrice = 0

                elif filter["filterType"] == "MARKET_LOT_SIZE":
                    minPriceMarket = float(filter["minQty"])

                    if "e" not in str(minPriceMarket):
                        if minPriceMarket < 1:
                            minPriceMarket = len(list(str(minPriceMarket).split(".")[1]))
                        else:
                            minPriceMarket = 0
                    else:
                        minPriceMarket = int(str(minPriceMarket).split("-")[-1])
                elif filter["filterType"] == "MAX_NUM_ALGO_ORDERS":
                    MAX_NUM_ALGO_ORDERS = filter["limit"]
            result[exch["symbol"]] = [minQty, minPrice, minPriceMarket, exch["onboardDate"], MAX_NUM_ALGO_ORDERS]

    return result
exchangeInfo = getExchangeInfo()

def transformationPrice(price, x):
    if x == 0:
        return int(price)


    price = str(price).replace(",", ".")

    try:
        full = price.split(".")[0]
        drob = price.split(".")[1]

        price = f"{full}.{drob[:x]}"
    except:
        pass

    return float(price)

def precWithPrice(price, prec):
    if prec == "":
        return False
    return float(price) * (float(prec) / 100 + 1)

def precWithoutPrice(price, prec):
    if prec == "":
        return False
    return float(price) - (float(price) * (float(prec) / 100))

def get_klines(symbol, lklines, interval, ex):
    stime = 0

    if not lklines:
        klines = []
        while True:
            if stime == 0:
                klines = trading_api.get_klines(symbol, interval, ex)
                stime = 1
            else:
                stime = klines[-1][0]
                # print(symbol, datetime.datetime.fromtimestamp(int(stime)/1000))

                try:
                    nk = trading_api.get_klines(symbol, interval, stime)
                except:
                    send_msg(f"{symbol} ошибка при получении свеч, повтор попытки!")
                    time.sleep(1)
                    continue

                del nk[0]
                for kline in nk:
                    klines.append(kline)

                if len(nk) < 499:
                    break
    else:
        del lklines[-1]
        lk = 0
        while True:
            klines = lklines
            stime = klines[-1][0]
            # print(symbol, datetime.datetime.fromtimestamp(int(stime) / 1000))
            while True:
                try:
                    nklines = trading_api.get_klines(symbol, interval, stime)
                    break
                except Exception as err:
                    send_msg(f"{err} {extract_tb(exc_info()[2])}")
                    send_msg(f"{symbol} ошибка при получении свеч, повтор попытки!")
                    continue

            if len(nklines) < 500 or (lk != 0 and lk == klines[-1][0]):
                del klines[-1]
                klines = klines + nklines
                break
            else:
                del nklines[0]
                klines = klines + nklines
                break
            lk = klines[-1][0]
    lt = 0
    try:
        lt = str(lklines[-1][0])
    except:
        pass

    if lt != str(klines[-1][0]):
        klines_n = []
        for kline in klines:
            klines_n.append([float(kline[0]), float(kline[1]), float(kline[2]), float(kline[3]), float(kline[4]), float(kline[5])])

        stime = time.time()
        Settings.saveKlines(symbol, klines_n, interval)

    return klines

def check_stop():
    stop_orders = len(trading_api.get_stop_orders(symbol))
    distant_price = 0
    distant_setup = ""
    if stop_orders >= exchangeInfo[symbol][4]:
        for ttl in settings.copy().keys():
            if settings[ttl]["symbol"] == symbol and settings[ttl]["status"] == "ON" and not settings[ttl]["trigger"]:
                if cross == "long" and symbols_side[symbol] != "short":
                    if settings[ttl]["priceOpen"] > distant_price or distant_price == 0:
                        distant_price = settings[ttl]["priceOpen"]
                        distant_setup = ttl

                if cross == "short" and symbols_side[symbol] != "long":
                    if settings[ttl]["priceOpen"] < distant_price or distant_price == 0:
                        distant_price = settings[ttl]["priceOpen"]
                        distant_setup = ttl

        if distant_price != 0:
            misc.send_msg(f"{title} выставлено слишком много стоп-ордеров, отмена самого дальнего..")
            trading_api.cancel_order(settings[distant_setup]["orderId"])
            settings[distant_setup] = get_settings(symbol)

def send_msg(msg="", send=True):
    msg = f"[{str(datetime.datetime.today()).split('.')[0]}] {str(msg)}"

    if send:
        print(msg)
    Settings.saveLog(msg)

def get_realizedPnl(symbol, orders):
    trades = list(reversed(trading_api.get_account_trades(symbol)))[:500]

    realizedPnl = 0
    commission = 0
    for trade in trades:
        if trade["orderId"] in orders:
            realizedPnl += float(trade["realizedPnl"])
            commission += float(trade["commission"])

    realizedPnl -= commission
    realizedPnl = round(realizedPnl, 5)
    send_msg(f'{symbol} Прибыль: {realizedPnl}')

    return realizedPnl

def get_sar(klines, sett, x):
    trend = 1               # тренд

    sar_acc_begin = sett[0]   # начальное ускорение
    sar_acc_step = sett[1]    # шаг ускорения
    sar_acc_max = sett[2]      # максимально ускорение

    SAR = float(klines[0][3])
    SAR_pr = SAR
    ext = SAR

    sar_acc = 0

    first_sar = 0

    kline_first = klines[0]
    open1 = kline_first[1]
    high1 = kline_first[2]
    low1 = kline_first[3]
    close1 = kline_first[4]

    kline_second = klines[1]
    open2 = kline_second[1]
    high2 = kline_second[2]
    low2 = kline_second[3]
    close2 = kline_second[4]

    point_down = low1
    point_up = high1

    # first_kline = "long"
    # if klines[0][1] > klines[0][4]: first_kline = "short"
    #
    # if first_kline == "long" and klines[0][3] <= klines[1][3]: first_sar = klines[0][3]
    # elif first_kline == "short" and klines[0][2] >= klines[1][2]: first_sar = klines[0][2]
    # else:
    #     if first_kline == "long": first_sar = klines[0][3]
    #     elif first_kline == "short": first_sar = klines[0][2]

    if high2 > high1 and low2 > low1: first_sar = point_down
    elif high2 < high1 and low2 < low1: first_sar = point_up

    elif high2 > high1 and low2 < low1:
        if open1 < close1 and open2 < close2: first_sar = point_up
        elif open1 < close1 and open2 > close2: first_sar = point_down
        elif open1 > close1 and open2 < close2: first_sar = point_up
        elif open1 > close1 and open2 > close2: first_sar = point_down

    elif high2 < high1 and low2 > low1:
        if open1 < close1 and open2 < close2: first_sar = point_down
        elif open1 < close1 and open2 > close2: first_sar = point_up
        elif open1 > close1 and open2 < close2: first_sar = point_down
        elif open1 > close1 and open2 > close2: first_sar = point_up



    result = [0, first_sar]
    for kline in klines[2:]:
        high_for_save = float(kline[2])
        low_for_save = float(kline[3])
        # проверка смены тренда с лонга на шорт !!! =
        if trend == 1 and low_for_save <= SAR:
            trend = 0
            sar_acc = sar_acc_begin
            SAR_pr = SAR
            if high_for_save >= ext:
                SAR = high_for_save
            else:
                SAR = ext

            ext = low_for_save
            result.append(round(SAR, x))
            continue

        # проверка смены тренда с шорта на лонг !!! =
        if trend == 0 and high_for_save >= SAR:
            trend = 1
            sar_acc = sar_acc_begin
            SAR_pr = SAR
            if low_for_save <= ext:
                SAR = low_for_save
            else:
                SAR = ext

            ext = high_for_save
            result.append(round(SAR, x))
            continue

        if trend == 1 and low_for_save > SAR:                      # условия продолжения АП-тренда
            if high_for_save > ext:                                 # условия обновления максимума
                ext = high_for_save
                sar_acc = sar_acc + sar_acc_step
                if sar_acc > sar_acc_max:
                    sar_acc = sar_acc_max

            SAR_pr = SAR
            SAR = SAR + sar_acc * (ext - SAR)                       # расчет SAR для АП-тренда
            if low_for_save < SAR and low_for_save >= SAR_pr:
                SAR = low_for_save

        elif trend == 0 and high_for_save < SAR:                   # условия продолжения ДАУН-тренда
            if low_for_save < ext:                                  # условия обновления минимума
                ext = low_for_save
                sar_acc = sar_acc + sar_acc_step
                if sar_acc > sar_acc_max:
                    sar_acc = sar_acc_max

            SAR_pr = SAR
            SAR = SAR - sar_acc * (SAR - ext)                       # расчет SAR для ДАУН-тренда
            if high_for_save > SAR and high_for_save <= SAR_pr:
                SAR = high_for_save

        result.append(round(SAR, x))

    return result

def crossing(klines, sar):
    if sar[-2] >= float(klines[-2][2]) and sar[-1] <= float(klines[-1][3]):
        # print(datetime.datetime.fromtimestamp(float(klines[-(1)][0]) / 1000))
        return "long"
    elif sar[-2] <= float(klines[-2][3]) and sar[-1] >= float(klines[-1][2]):
        # print(datetime.datetime.fromtimestamp(float(klines[-(1)][0])/1000))
        return "short"
    else:
        return False

def get_p(x, y):
    if x == 0:
        return 1

    result = "0."
    for i in range(x-1):
        result += "0"
    result += str(y)

    return float(result)

def get_nowTP(title, klines, sar, tp):
    klines = list(reversed(klines))
    sar = list(reversed(sar))

    high = 0
    low = 0

    for i in range(len(klines)):
        if float(klines[i][2]) > high or high == 0:
            high = float(klines[i][2])

        if float(klines[i][3]) < low or low == 0:
            low = float(klines[i][3])

        if sar[i] >= float(klines[i][2]) and sar[i + 1] <= float(klines[i + 1][3]):
            # print(title, f'{str(datetime.datetime.today()).split(".")[0]}', datetime.datetime.fromtimestamp(float(klines[i][0]) / 1000), "short", i, low)
            if tp < low:
                return False
            else:
                return True

        if sar[i] <= float(klines[i][3]) and sar[i + 1] >= float(klines[i + 1][2]):
            # print(title, f'{str(datetime.datetime.today()).split(".")[0]}', datetime.datetime.fromtimestamp(float(klines[i][0]) / 1000), "long", i, high)
            if tp > high:
                return False
            else:
                return True

def get_lastSL(title, symbol, klines, sar, ticks_to_open, p, tp, sl):
    klines = list(reversed(klines))
    sar = list(reversed(sar))

    skipNowTrand = False
    priceTP = 0
    priceSL = 0
    i_tp = 0
    i_sl = 0

    high = 0
    low = 0

    pps = 0
    for i in range(ticks_to_open):
        pps += p

    trand = {"highs": [], "lows": [], "side": ""}
    trand_klines = []
    ep = 0
    for i in range(len(klines)):
        if not skipNowTrand:
            trand1 = sar[i] > float(klines[i][1]) and sar[i + 1] < float(klines[i + 1][4])
            trand2 = sar[i] < float(klines[i][1]) and sar[i + 1] > float(klines[i + 1][4])
            if trand1 or trand2:
                # print(sar[i], float(klines[i][2]), sar[i + 1], float(klines[i + 1][3]))
                skipNowTrand = True
                # print(title, f'{str(datetime.datetime.today()).split(".")[0]}', datetime.datetime.fromtimestamp(float(klines[i][0]) / 1000), "skipNowTrand", trand1, trand2)

        else:
            if float(klines[i][2]) > high or high == 0:
                i_sl = i
                high = float(klines[i][2])

            if float(klines[i][3]) < low or low == 0:
                i_tp = i
                low = float(klines[i][3])

            trand["lows"].append(float(klines[i][3]))
            trand["highs"].append(float(klines[i][2]))

            if sar[i] >= float(klines[i][1]) and sar[i + 1] <= float(klines[i + 1][4]):
                trand["side"] = "short"
                ep = sar[i + 1] - pps
                priceTP = precWithoutPrice(ep, tp)
                priceSL = precWithPrice(ep, sl)
                trand_klines.append(klines[i])

                # print(title, f'{str(datetime.datetime.today()).split(".")[0]}', datetime.datetime.fromtimestamp(float(klines[i][0]) / 1000), "short", i, low, priceTP, priceSL, len(klines), len(sar), i_tp, i_sl)
                break

            if sar[i] <= float(klines[i][4]) and sar[i + 1] >= float(klines[i + 1][1]):
                trand["side"] = "long"
                ep = sar[i + 1] + pps
                priceTP = precWithPrice(ep, tp)
                priceSL = precWithoutPrice(ep, sl)
                trand_klines.append(klines[i])

                # print(title, f'{str(datetime.datetime.today()).split(".")[0]}', datetime.datetime.fromtimestamp(float(klines[i][0]) / 1000), "long", i, high, priceTP, priceSL, len(klines), len(sar), i_tp, i_sl)
                break

            trand_klines.append(klines[i])

    # print(start_kline_trand)
    trand = {"highs": list(reversed(trand["highs"])), "lows": list(reversed(trand["lows"])), "side": trand["side"]}
    trand_klines = list(reversed(trand_klines))
    for skline in trand_klines:
        startTime = int(skline[0])
        mkline = int((klines[0][0] - klines[1][0]) / 300000)
        klines_5m = trading_api.get_klines(symbol, "5m", startTime)[:mkline]

        isOpen = False
        for kline in klines_5m:
            if not isOpen:
                if (trand["side"] == "long" and float(kline[3]) >= ep) or (trand["side"] == "short" and float(kline[2]) <= ep):
                    isOpen = True

            if isOpen:
                if trand["side"] == "long":
                    if float(kline[2]) >= priceTP:
                        return False
                    if float(kline[3]) <= priceSL:
                        return True

                elif trand["side"] == "short":
                    if float(kline[3]) <= priceTP:
                        return False
                    if float(kline[2]) >= priceSL:
                        return True
    return True

if __name__ == '__main__':
    # send_msg("test")
    # # print(exchangeInfo["ADAUSDT"])
    symbol = "DOGEUSDT"
    interval = "3d"
    # tp = 0.4
    # sl = 6
    # print(getExchangeInfo()[symbol][1])
    klines = get_klines(symbol, Settings.getKlines(symbol, interval), interval, exchangeInfo[symbol][-1])
    klines = Settings.getKlines(symbol, interval)[:-146]
    print("старт:", datetime.datetime.fromtimestamp(float(klines[-2][0]) / 1000), klines[-2])
    #
    sar = get_sar(klines, [0.02, 0.02, 0.2], exchangeInfo[symbol][1])
    print(sar[-2])