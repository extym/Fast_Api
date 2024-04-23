# -*- coding: utf-8 -*-

import time
import datetime
import trading_api
import misc
import Settings
from config import *
from config import couples as cpls
from sys import exc_info
from traceback import extract_tb
import websocket
import ast
import threading

delay_info = 900

exchangeInfo = misc.getExchangeInfo()

conn_prices = "0"
prices = {}
def on_message_price(ws, message):
    global prices
    try:
        event = ast.literal_eval(message.replace('false', "False").replace('true', "True"))
        if "USDT" in event["s"] and event["s"] in exchangeInfo.keys():
            prices[event["s"]] = misc.transformationPrice((float(event["a"]) + float(event["b"])) / 2, exchangeInfo[event["s"]][1])
    except Exception as err:
        misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
def on_error_price(ws, error):
    global conn_prices
    try:
        ws.close()
    except:
        pass

    # conn_prices = "1"
    # misc.send_msg("price close")

def on_close(ws, close_status_code, close_msg):
    misc.send_msg(f"[WEBSOCKET] closed")

    ws.close
    time.sleep(5)

    conn_prices = "1"
def on_open_price(ws):
    global conn_prices
    conn_prices = "2"
    misc.send_msg(f"[WEBSOCKET] launched")
def start_market_price():
    global conn_prices, prices

    try:
        ws = websocket.WebSocketApp(f"wss://fstream.binance.com/ws/!bookTicker", on_message=on_message_price, on_error=on_error_price, on_open=on_open_price, on_close=on_close)
        ws.run_forever()
    except:
        conn_prices = "1"

    # conn_prices = "2"
    # while True:
    #     try:
    #         prices = trading_api.get_price()
    #     except:
    #         pass
    #     time.sleep(3)

klines_all = {}
def get_all_klines():
    global klines_all

    kl_all = []
    for title, couple in couples.copy().items():
        if couple["enable"] == "ON":
            symbol = couple["ticker"]
            ttl = f"{symbol}_{couple['timeFrame']}"
            if ttl not in kl_all:
                misc.send_msg(f'{ttl} ..')
                trading_api.change_lev(symbol, couple["LEV"])
                trading_api.set_isolate(symbol)

                misc.get_klines(symbol, Settings.getKlines(symbol, couple["timeFrame"]), couple["timeFrame"], exchangeInfo[symbol][3])
                misc.send_msg(f"{symbol} OK")
                kl_all.append(ttl)

    misc.send_msg("Все свечи собраны")
    print("")

def start_bot():
    global conn_prices, klines_all, prices

    settings = {}

    start_balances = {}
    lastKlines = {}
    lastKlinesSend = {}
    fstarts = {}
    symbol = ""
    def get_settings(symbol, lastSL=False):
        return {
            "symbol": symbol,
            "status": "OFF",
            "lastSL": lastSL,
            "lastKline": 0,
            "trigger": "",
            "priceTP": 0,
            "priceSL": 0,
            "priceOpen": 0,
            "priceTrigger": 0,
            "size": 0,
            "size_lev": 0,
            "side": "",
            "orderId": 0,
            "TPId": 0,
            "SLId": 0,
            "lastSar": 0,
            "orders": [],
            "size_position": 0,
            "entry_price": 0,
            "filled_orders": []
        }

    def profit(symbol, title, orders):
        pnl = misc.get_realizedPnl(symbol, orders)
        order_time = str(datetime.datetime.today()).split('.')[0].replace(' ', ';')
        balance = misc.transformationPrice(trading_api.get_balance(), 2)

        # couples[title]["startBalance"] += pnl

        if couples[title]["saving_funds"]:
            save_balance = start_balances[title] * 1.5
            if couples[title]["startBalance"] >= save_balance:
                profit_balance = misc.transformationPrice((couples[title]["startBalance"] - start_balances[title]) * 0.5, 4)
                trading_api.transferFromFutures(profit_balance)
                couples[title]["startBalance"] -= profit_balance
                start_balances[title] = couples[title]["startBalance"]
                misc.send_msg(f"{title} прибыль {profit_balance}$ переведено на спот!")

        couple = couples[title]

        history = f'{order_time};{symbol};{settings[title]["side"]};{couple["timeFrame"]};{str(couple["SAR"])};{get_tp(symbol, couple["SAR"])};{couple["SL"]};{pnl};{balance}'
        misc.send_msg(f"{symbol} {history}")
        Settings.saveHistory(history)
        Settings.saveBalance(symbol, balance)

        Settings.saveCouples(couples)

    def get_klines(symbol, interval):
        if f"{symbol}_{interval}" in klines_all.keys():
            klines = misc.get_klines(symbol, klines_all[f"{symbol}_{interval}"]["klines"], interval, exchangeInfo[symbol][3])
        else:
            klines = misc.get_klines(symbol, Settings.getKlines(symbol, interval), interval, exchangeInfo[symbol][3])

        return {
            "klines": klines,
            "newKline": (float(klines[-1][0]) + abs(float(klines[-2][0]) - float(klines[-3][0]))) / 1000 + 1,
        }

    def get_tp(symbol, sar):
        return tps[symbol]["TP"][str(sar)]

    last_sides = {}
    last_upd_msg = 0

    while True:




        for title, couple in couples.copy().items():
            try:

                send_status = False
                if time.time() - last_upd_msg >= delay_info:
                    send_status = True
                    last_upd_msg = time.time()

                if send_status: misc.send_msg(f"Статус OK")

                if couple["enable"] == "ON":

                    time.sleep(0.3)
                    prices = trading_api.get_price()

                    if title not in start_balances.keys():
                        start_balances[title] = couple["startBalance"]

                    if title not in lastKlines.keys():
                        lastKlines[title] = 0
                        lastKlinesSend[title] = 0

                    if title not in last_sides:
                        last_sides[title] = ""

                    if title not in fstarts:
                        fstarts[title] = []

                    # if conn_prices == "1":
                    #     threading.Thread(target=start_market_price).start()
                    #     # misc.send_msg(f"подключение..")
                    #     conn_prices = "2"

                    symbol = couple["ticker"]

                    if title not in list(settings.keys()):
                        settings[title] = get_settings(symbol)

                    if symbol not in prices.keys():
                        misc.send_msg(f"{symbol} текущая цена не получена")
                        continue
                    if send_status: misc.send_msg(f"Статус OK 2")
                    price = trading_api.get_price(symbol)
                    klines = get_klines(symbol, couple["timeFrame"])["klines"]#[:-10]
                    sar_all = misc.get_sar(klines, couple["SAR"], exchangeInfo[symbol][1])
                    sar = sar_all[-2]

                    if "toTrand" not in fstarts[title]:
                        toTrand = False
                        if (sar_all[-1] <= float(klines[-1][3]) and sar_all[-2] <= float(klines[-2][3])) or (sar_all[-1] >= float(klines[-1][2]) and sar_all[-2] >= float(klines[-2][2])):
                            toTrand = True
                    else:
                        toTrand = fstarts[title]

                    cross = ""
                    if sar <= float(klines[-2][3]):
                        cross = "short"

                    if sar >= float(klines[-2][2]):
                        cross = "long"

                    if settings[title]["status"] == "OFF":
                        if send_status: misc.send_msg(f"Статус OK 3")
                        try:
                            if cross and lastKlines[title] != klines[-1][0] and toTrand:
                                stop_orders = len(trading_api.get_stop_orders(symbol))
                                if stop_orders < exchangeInfo[symbol][4]:
                                    if cross == "long" and last_sides[title] != "long":
                                        p = misc.get_p(exchangeInfo[symbol][1], 1)
                                        psar = round(sar, exchangeInfo[symbol][1])

                                        pps = 0
                                        for i in range(couple["ticks_to_open"]):
                                            pps += p

                                        price = misc.transformationPrice(round(psar + p, exchangeInfo[symbol][1]), exchangeInfo[symbol][1])
                                        stopPrice = misc.transformationPrice(round(price + pps, exchangeInfo[symbol][1]), exchangeInfo[symbol][1])

                                        # psar = trading_api.get_price(symbol)
                                        # price = psar

                                        misc.send_msg(f"{title} выставление {cross} ордера..")

                                        if settings[title]["lastSL"]:
                                            size = misc.transformationPrice(couple["startBalance"] / price * couple["multiplier_size"], exchangeInfo[symbol][0])
                                            misc.send_msg(f"{title} используем множитель объёма {couple['multiplier_size']}")
                                            misc.send_msg(f'{title} {couple["startBalance"]} / {price} * {couple["multiplier_size"]} * {couple["LEV"]}')
                                        else: size = misc.transformationPrice(couple["startBalance"] / price, exchangeInfo[symbol][0])

                                        size_lev = misc.transformationPrice(size * couple["LEV"], exchangeInfo[symbol][0])

                                        if size_lev == 0:
                                            misc.send_msg(f'{title} слишком маленький объём!')
                                            continue

                                        price_now = prices[symbol]

                                        if price <= price_now or (sar_all[-1] < float(klines[-1][3]) and price >= price_now):
                                            order = trading_api.long_market(symbol, size_lev)
                                            misc.send_msg(f"{title} выставлен маркет ордер")
                                        else:
                                            try:
                                                order = trading_api.stop_long(symbol, price, stopPrice, size_lev)
                                                misc.send_msg(f"{title} выставлен stop_long")
                                            except Exception as err:
                                                if "Order would immediately trigger" in str(err):
                                                    order = trading_api.long(symbol, price, size_lev)
                                                    misc.send_msg(f"{title} выставлен long")
                                                elif "Margin is" in str(err):
                                                    try:
                                                        order = trading_api.stop_market_long(symbol, price, size_lev)
                                                        misc.send_msg(f"{title} выставлен stop_market_long")
                                                    except:
                                                        misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
                                                        continue
                                                else:
                                                    misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
                                                    continue

                                        settings[title]["side"] = cross
                                        settings[title]["priceOpen"] = price
                                        settings[title]["priceTrigger"] = stopPrice
                                        settings[title]["priceTP"] = misc.transformationPrice(misc.precWithPrice(price, get_tp(symbol, couple["SAR"])), exchangeInfo[symbol][1])
                                        settings[title]["priceSL"] = misc.transformationPrice(misc.precWithoutPrice(price, couple["SL"]), exchangeInfo[symbol][1])
                                        settings[title]["status"] = "ON"
                                        settings[title]["orderId"] = order["orderId"]
                                        settings[title]["size"] = size
                                        settings[title]["lastSar"] = sar
                                        settings[title]["size_lev"] = size_lev

                                        last_sides[title] = cross
                                        lastKlines[title] = klines[-1][0]

                                        if "toTrand" not in fstarts[title]:
                                            fstarts[title].append("toTrand")

                                        Settings.saveOrder(f"{str(datetime.datetime.today()).split('.')[0].replace(' ', ';')};{str(couple['SAR'])};{get_tp(symbol, couple['SAR'])};{couple['SL']}")

                                        misc.send_msg(f"{title} выставлен {cross} ордер на открытие {price} {stopPrice} {psar} {size_lev} {price_now} {round(size * price, 2)}$ {round(size_lev * price, 2)}$")

                                    elif cross == "short" and last_sides[title] != "short":
                                        p = misc.get_p(exchangeInfo[symbol][1], 1)
                                        psar = round(sar, exchangeInfo[symbol][1])

                                        pps = 0
                                        for i in range(couple["ticks_to_open"]): pps += p

                                        price = misc.transformationPrice(round(psar - p, exchangeInfo[symbol][1]), exchangeInfo[symbol][1])
                                        stopPrice = misc.transformationPrice(round(price - pps, exchangeInfo[symbol][1]), exchangeInfo[symbol][1])

                                        misc.send_msg(f"{title} выставление {cross} ордера..")


                                        if settings[title]["lastSL"]:
                                            size = misc.transformationPrice(couple["startBalance"] / price * couple["multiplier_size"], exchangeInfo[symbol][0])
                                            misc.send_msg(f"{title} используем множитель объёма {couple['multiplier_size']}")
                                            misc.send_msg(f'{title} {couple["startBalance"]} / {price} * {couple["multiplier_size"]} * {couple["LEV"]}')
                                        else:
                                            size = misc.transformationPrice(couple["startBalance"] / price, exchangeInfo[symbol][0])

                                        size_lev = misc.transformationPrice(size * couple["LEV"], exchangeInfo[symbol][0])

                                        if size_lev == 0:
                                            misc.send_msg(f'{title} слишком маленький объём!')
                                            continue

                                        price_now = prices[symbol]

                                        if price >= price_now or (sar_all[-1] > float(klines[-1][2]) and price <= price_now):
                                            order = trading_api.short_market(symbol, size_lev)
                                            misc.send_msg(f"{title} выставлен маркет ордер")
                                        else:
                                            try:
                                                order = trading_api.stop_short(symbol, price, stopPrice, size_lev)
                                                misc.send_msg(f"{title} выставлен stop_short")
                                            except Exception as err:
                                                if "Order would immediately trigger" in str(err):
                                                    order = trading_api.short(symbol, price, size_lev)
                                                    misc.send_msg(f"{title} выставлен short")
                                                elif "Margin is" in str(err):
                                                    try:
                                                        order = trading_api.stop_market_short(symbol, price, size_lev)
                                                        misc.send_msg(f"{title} выставлен stop_market_short")
                                                    except:
                                                        misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
                                                        continue
                                                else:
                                                    misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
                                                    continue

                                        settings[title]["side"] = cross
                                        settings[title]["priceOpen"] = price
                                        settings[title]["priceTrigger"] = stopPrice
                                        settings[title]["priceTP"] = misc.transformationPrice(misc.precWithoutPrice(price, get_tp(symbol, couple["SAR"])), exchangeInfo[symbol][1])
                                        settings[title]["priceSL"] = misc.transformationPrice(misc.precWithPrice(price, couple["SL"]), exchangeInfo[symbol][1])
                                        settings[title]["status"] = "ON"
                                        settings[title]["orderId"] = order["orderId"]
                                        settings[title]["size"] = size
                                        settings[title]["lastSar"] = sar
                                        settings[title]["size_lev"] = size_lev

                                        last_sides[title] = cross
                                        lastKlines[title] = klines[-1][0]

                                        if "toTrand" not in fstarts[title]:
                                            fstarts[title].append("toTrand")

                                        Settings.saveOrder(f"{str(datetime.datetime.today()).split('.')[0].replace(' ', ';')};{str(couple['SAR'])};{get_tp(symbol, couple['SAR'])};{couple['SL']}")

                                        misc.send_msg(f"{title} выставлен {cross} ордер на открытие {price} {stopPrice} {psar} {size_lev} {price_now} {round(size * price, 2)}$ {round(size_lev * price, 2)}$")
                                else:
                                    misc.send_msg(f"{title} слишком много открытых ордеров")
                                    settings[title] = get_settings(symbol)
                                    continue

                                settings[title]["lastKline"] = klines[-1][0]

                        except Exception as err:
                            misc.send_msg(f"{err} {extract_tb(exc_info()[2])}")
                            if "Margin is insufficient" not in str(err):
                                continue
                        if send_status: misc.send_msg(f"Статус OK 4")

                    if settings[title]["status"] == "ON":
                        if send_status: misc.send_msg(f"Статус OK 5")
                        if not settings[title]["trigger"]:
                            price = trading_api.get_price(symbol)

                            order_info = trading_api.get_order(symbol, settings[title]["orderId"])

                            if order_info["status"] == "FILLED":
                                size = misc.transformationPrice(float(order_info["origQty"]), exchangeInfo[symbol][0])
                                misc.send_msg(f"{title} исполенный {settings[title]['side']} объём ордера {size}")

                                price_tp = misc.transformationPrice(settings[title]["priceTP"], exchangeInfo[symbol][1])
                                price_sl = misc.transformationPrice(settings[title]["priceSL"], exchangeInfo[symbol][1])

                                if settings[title]['side'] == "long":
                                    # проверка тп после открытия позиции
                                    if price_tp <= float(klines[-1][2]):
                                        misc.send_msg(f"{title} цена достигла тп - закрываю по маркету")
                                        trading_api.short_market(symbol, settings[title]["size"], True)
                                        settings[title] = get_settings(symbol, settings[title]["lastSL"])
                                        continue

                                    # выставление сетки
                                    for i in range(len(couple["steps"])):
                                        size_open_step = misc.transformationPrice(settings[title]["size_lev"] * couple["size_steps"][i], exchangeInfo[symbol][0])
                                        price_open_step = misc.transformationPrice(misc.precWithoutPrice(settings[title]["priceOpen"], couple["steps"][i]), exchangeInfo[symbol][1])
                                        misc.send_msg(f"{title} выставлен {settings[title]['side']} ордер на усреднение {size_open_step, price_open_step}")

                                        while True:
                                            try:
                                                order_step = trading_api.long(symbol, price_open_step, size_open_step)
                                                break
                                            except Exception as err:
                                                misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                                time.sleep(3)

                                        settings[title]["orders"].append(order_step["orderId"])

                                    while True:
                                        try:
                                            order_tp = trading_api.short(symbol, price_tp, size, False)
                                            break
                                        except Exception as err:
                                            misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                            time.sleep(3)

                                    while True:
                                        try:
                                            order_sl = trading_api.stop_market_short(symbol, price_sl, size, False)
                                            break
                                        except Exception as err:
                                            misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                            time.sleep(3)

                                elif settings[title]['side'] == "short":
                                    # проверка тп после открытия позиции
                                    if price_tp >= float(klines[-1][3]):
                                        misc.send_msg(f"{title} цена достигла тп - закрываю по маркету")
                                        trading_api.long_market(symbol, settings[title]["size"], True)
                                        settings[title] = get_settings(symbol, settings[title]["lastSL"])
                                        continue

                                    # выставление сетки
                                    for i in range(len(couple["steps"])):
                                        size_open_step = misc.transformationPrice(settings[title]["size_lev"] * couple["size_steps"][i], exchangeInfo[symbol][0])
                                        price_open_step = misc.transformationPrice(misc.precWithPrice(settings[title]["priceOpen"], couple["steps"][i]), exchangeInfo[symbol][1])
                                        misc.send_msg(f"{title} выставлен {settings[title]['side']} ордер на усреднение {size_open_step, price_open_step}")

                                        while True:
                                            try:
                                                order_step = trading_api.short(symbol, price_open_step, size_open_step)
                                                break
                                            except Exception as err:
                                                misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                                time.sleep(3)

                                        settings[title]["orders"].append(order_step["orderId"])


                                    while True:
                                        try:
                                            order_tp = trading_api.long(symbol, price_tp, size, False)
                                            if not order_tp: misc.send_msg(f"{title} {symbol, price_tp, size, order_tp}")
                                            break
                                        except Exception as err:
                                            misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                            time.sleep(3)

                                    while True:
                                        try:
                                            order_sl = trading_api.stop_market_long(symbol, price_sl, size, False)
                                            if not order_sl: misc.send_msg(f"{title} {symbol, price_sl, size, order_sl}")
                                            break
                                        except Exception as err:
                                            misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")
                                            time.sleep(3)

                                misc.send_msg(f"{title} TP: {price_tp} {size}")
                                misc.send_msg(f"{title} SL: {price_sl} {size}")

                                settings[title]["TPId"] = order_tp["orderId"]
                                settings[title]["SLId"] = order_sl["orderId"]
                                settings[title]["size"] = size
                                settings[title]["size_position"] = size
                                settings[title]["trigger"] = "1"

                            else:
                                if settings[title]["lastSar"] != sar:
                                    misc.send_msg(f"{title} новая свеча, перестановка ордера")
                                    trading_api.cancel_order(symbol, settings[title]["orderId"])
                                    settings[title] = get_settings(symbol, settings[title]["lastSL"])
                                    last_sides[title] = ""
                                    continue
                        elif settings[title]["trigger"] == "1":
                            order_sl = trading_api.get_order(symbol, settings[title]["SLId"])
                            if order_sl["status"] == "FILLED":
                                trading_api.cancel_order(symbol, settings[title]["TPId"])
                                for order_step in settings[title]["orders"]: trading_api.cancel_order(symbol, order_step)
                                time.sleep(0.1)

                                misc.send_msg(f"{title} {settings[title]['side']} позиция закрыта по SL")

                                size_position = 0
                                orders_step = trading_api.get_orders(symbol)
                                for order_step in orders_step:
                                    if order_step["orderId"] in settings[title]["orders"]:
                                        size_position += float(order_step["executedQty"])
                                size_position = abs(misc.transformationPrice(size_position, exchangeInfo[symbol][0]))

                                if size_position > settings[title]["size_position"]:
                                    size_close = abs(misc.transformationPrice(size_position - settings[title]["size_position"], exchangeInfo[symbol][0]))
                                    if settings[title]['side'] == "long": trading_api.short_market(symbol, size_close, True)
                                    elif settings[title]['side'] == "short": trading_api.long_market(symbol, size_close, True)
                                    misc.send_msg(f"{symbol} произошло дозакрытие позиции SL {size_close}")

                                profit(symbol, title, [settings[title]["orderId"], settings[title]["SLId"]])
                                settings[title] = get_settings(symbol, True)
                                continue

                            if settings[title]["TPId"] != 0:
                                order_tp = trading_api.get_order(symbol, settings[title]["TPId"])
                                if order_tp["status"] == "FILLED":
                                    trading_api.cancel_order(symbol, settings[title]["SLId"])
                                    for order_step in settings[title]["orders"]: trading_api.cancel_order(symbol, order_step)

                                    misc.send_msg(f"{title} {settings[title]['side']} позиция закрыта по TP!")
                                    profit(symbol, title, [settings[title]["orderId"], settings[title]["TPId"]])
                                    settings[title] = get_settings(symbol)
                                    continue
                                else:
                                    if float(order_tp["executedQty"]) > 0:
                                        trading_api.cancel_order(symbol, settings[title]["TPId"])
                                        trading_api.cancel_order(symbol, settings[title]["SLId"])
                                        order_tp = trading_api.get_order(symbol, settings[title]["TPId"])
                                        size = abs(float(order_tp["origQty"]) - float(order_tp["executedQty"]))
                                        if size > 0:
                                            if settings[title]['side'] == "long":
                                                order_close = trading_api.short_market(symbol, size, True)
                                            elif settings[title]['side'] == "short":
                                                order_close = trading_api.long_market(symbol, size, True)

                                            for order_step in settings[title]["orders"]: trading_api.cancel_order(symbol, order_step)
                                            misc.send_msg(f"{title} {settings[title]['side']} позиция закрыта по TP")
                                            profit(symbol, title, [settings[title]["orderId"], settings[title]["TPId"], order_close["orderId"]])
                                            settings[title] = get_settings(symbol)
                                            continue

                            # перевыставление тп и сл
                            orders_open = trading_api.get_orders(symbol, False)
                            size_position = settings[title]["size"]
                            entry_price = 0

                            for order_open in orders_open:
                                if order_open["orderId"] in settings[title]["orders"]:
                                    if order_open["orderId"] not in settings[title]["filled_orders"]:
                                        misc.send_msg(f"{title} исполнен {settings[title]['side']} ордер на усреднение")
                                        settings[title]["filled_orders"].append(order_open["orderId"])

                                    size_position += float(order_open["executedQty"])
                                    if entry_price == 0: entry_price = settings[title]["priceOpen"]
                                    else: entry_price = (entry_price * settings[title]["size_position"] + float(order_open["price"]) * float(order_open["executedQty"])) / size_position

                            size_position = misc.transformationPrice(size_position, exchangeInfo[symbol][0])
                            entry_price = misc.transformationPrice(entry_price, exchangeInfo[symbol][1])

                            if size_position != settings[title]["size_position"]:
                                trading_api.cancel_order(symbol, settings[title]["TPId"])
                                trading_api.cancel_order(symbol, settings[title]["SLId"])

                                price_tp = misc.transformationPrice(settings[title]["priceTP"], exchangeInfo[symbol][1])
                                price_sl = misc.transformationPrice(settings[title]["priceSL"], exchangeInfo[symbol][1])

                                if settings[title]['side'] == "long":
                                    order_tp = trading_api.short(symbol, price_tp, size_position, True)
                                    order_sl = trading_api.stop_market_short(symbol, price_sl, size_position, False)

                                elif settings[title]['side'] == "short":
                                    order_tp = trading_api.long(symbol, price_tp, size_position, True)
                                    order_sl = trading_api.stop_market_long(symbol, price_sl, size_position, False)

                                settings[title]["TPId"] = order_tp["orderId"]
                                settings[title]["SLId"] = order_sl["orderId"]
                                settings[title]["size_position"] = size_position

                                misc.send_msg(f"{title} {settings[title]['side']} позиция уреднена TP: {price_tp} SL: {price_sl}")
                        if send_status: misc.send_msg(f"Статус OK 7")


                        # if cross and cross != settings[title]['side'] and settings[title]['side']:

                        klines = get_klines(symbol, couple["timeFrame"])["klines"]  # [:-10]
                        sar_all = misc.get_sar(klines, couple["SAR"], exchangeInfo[symbol][1])
                        sar = sar_all[-2]
                        if send_status: misc.send_msg(f"Статус OK 8")
                        if (settings[title]['side'] == "short" and sar_all[-1] <= float(klines[-1][3])) or (settings[title]['side'] == "long" and sar_all[-1] >= float(klines[-1][2])):
                            if settings[title]["trigger"] == "1" and lastKlines[title] != klines[-1][0]:
                                trading_api.cancel_order(symbol, settings[title]["TPId"])
                                trading_api.cancel_order(symbol, settings[title]["SLId"])
                                trading_api.cancel_order(symbol, settings[title]["orderId"])
                                for order_step in settings[title]["orders"]: trading_api.cancel_order(symbol, order_step)

                                order_sl = trading_api.get_order(symbol, settings[title]["SLId"])

                                if abs(float(order_sl['executedQty'])) == 0:
                                    order_tp = trading_api.get_order(symbol, settings[title]["TPId"])

                                    size = misc.transformationPrice(abs(float(order_tp["origQty"]) - float(order_tp["executedQty"])), exchangeInfo[symbol][0])
                                    if size > 0:
                                        if settings[title]['side'] == "long":
                                            order_close = trading_api.short_market(symbol, size, True)
                                        elif settings[title]['side'] == "short":
                                            order_close = trading_api.long_market(symbol, size, True)

                                        misc.send_msg(f"{title} {settings[title]['side']} позиция закрыта по SAR {sar_all[-1]} {klines[-1][2], klines[-1][3]}")
                                        profit(symbol, title, [settings[title]["orderId"], order_close["orderId"]])
                                        settings[title] = get_settings(symbol)
                                    else:
                                        misc.send_msg(f"{title} {settings[title]['side']} ордер на открытие отменён по SAR {sar_all[-1]} {klines[-1][2], klines[-1][3]}")
                                        settings[title] = get_settings(symbol)

                        if send_status: misc.send_msg(f"Статус OK 9")
                elif couple["enable"] == "OFF":
                    if title in settings.keys():
                        del settings[title]

            except Exception as err:
                if "connection" not in str(err).lower():
                    misc.send_msg(f"{title} {err} {extract_tb(exc_info()[2])}")





if __name__ == '__main__':
    get_all_klines()

    threads = []

    threads.append(threading.Thread(target=start_market_price))
    threads.append(threading.Thread(target=start_bot))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()