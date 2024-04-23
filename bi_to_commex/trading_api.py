from config import *
import ast
from binance_f import RequestClient
from binance_f.model.constant import *
from binance_api import Binance
import time
import requests
import Settings
import datetime
from sys import exc_info
from traceback import extract_tb

mode = "o"

request_client = RequestClient(api_key=API_KEY, secret_key=API_SECRET)
bot_spot = Binance(API_KEY=API_KEY, API_SECRET=API_SECRET)

def long_market(symbol, quantity, reduceOnly=False):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=str(quantity), positionSide="LONG", reduceOnly=reduceOnly)
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=str(quantity), reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def short_market(symbol, quantity, reduceOnly=False):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.MARKET, quantity=str(quantity), positionSide="SHORT", reduceOnly=reduceOnly)
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.MARKET, quantity=str(quantity), reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def long(symbol, price, quantity, reduceOnly=False):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.LIMIT ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, positionSide="LONG", reduceOnly=reduceOnly)
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.LIMIT ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def short(symbol, price, quantity, reduceOnly=False):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.LIMIT ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, positionSide="SHORT", reduceOnly=reduceOnly)
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.LIMIT ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def stop_long(symbol, price, stopPrice, quantity):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, positionSide="LONG", stopPrice=str(stopPrice))
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP ,quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice))
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def stop_short(symbol, price, stopPrice, quantity):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP, quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, positionSide="SHORT", stopPrice=str(stopPrice))
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP, quantity=str(quantity), price=str(price), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice))
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def take_profit_long(symbol, stopPrice):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.TAKE_PROFIT_MARKET, stopPrice=str(stopPrice),  closePosition=True, positionSide="LONG")
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.TAKE_PROFIT_MARKET, stopPrice=str(stopPrice),  closePosition=True)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def take_profit_short(symbol, stopPrice):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.TAKE_PROFIT_MARKET, stopPrice=str(stopPrice),  closePosition=True, positionSide="SHORT")
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.TAKE_PROFIT_MARKET, stopPrice=str(stopPrice),  closePosition=True)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def stop_loss_long(symbol, stopPrice):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, stopPrice=str(stopPrice),  closePosition=True, positionSide="LONG")
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, stopPrice=str(stopPrice),  closePosition=True)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def stop_loss_short(symbol, stopPrice):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP_MARKET, stopPrice=str(stopPrice),  closePosition=True, positionSide="SHORT")
    else:
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP_MARKET, stopPrice=str(stopPrice),  closePosition=True,)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def get_positions(symbol=None):
    results = request_client.get_position_v2()
    results = ast.literal_eval(results.replace('"', "'").replace('false', "False").replace('true', "True"))
    ps = {}

    if symbol:
        for result in results:
            if result["symbol"] == symbol:
                if mode == "h":
                    if result["positionSide"] == "LONG":
                        ps["long"] = result
                    elif result["positionSide"] == "SHORT":
                        ps["short"] = result
                else:
                    return result
    else:
        return results

    return ps

def cancel_all_orders(symbol):
    try:
        request_client.cancel_all_orders(symbol=symbol)
    except:
        pass

def cancel_order(symbol, orderId):
    try:
        result = request_client.cancel_order(symbol=symbol, orderId=orderId)
        msg = f"[{str(datetime.datetime.today()).split('.')[0]}] {symbol} отменён ордер {orderId}"
        Settings.saveLog(msg)

        return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
    except:
        pass

def get_account_trades(symbol):
    result = request_client.get_account_trades(symbol=symbol)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def get_exchange_information():
    result = request_client.get_exchange_information()
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def get_open_orders(symbol):
    result = request_client.get_all_orders(symbol=symbol)

    orders = []

    result = ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
    for res in result:
        if res["status"] == "NEW":
            orders.append(res)

    return list(reversed(orders))

def get_orders(symbol, open_orders=False):
    result = request_client.get_all_orders(symbol=symbol)
    if open_orders:
        result = list(reversed(ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))))
        res = []

        for r in result:
            if r["status"] != "FILLED" and r["status"] != "CANCELED":
                res.append(r)
        return res

    else:
        return list(reversed(ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))))

def get_order(symbol, orderId):
    try:
        result = request_client.get_order(symbol=symbol, orderId=orderId)
        return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
    except:
        pass

def get_klines(symbol, interval, stime=None):
    if stime:
        result = request_client.get_candlestick_data(symbol=symbol, interval=interval, startTime=stime)
    else:
        result = request_client.get_candlestick_data(symbol=symbol, interval=interval)

    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def get_balance():
    result = request_client.get_balance_v2()
    for r in ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True")):
        if r["asset"] == "USDT":
            return float(r["balance"])

def change_lev(symbol, leverage):
    try:
        result = request_client.change_initial_leverage(symbol=symbol, leverage=str(leverage))
        return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
    except:
        pass

def set_isolate(symbol):
    try:
        result = request_client.change_margin_type(symbol=symbol, marginType=FuturesMarginType.ISOLATED)
        return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
    except:
        return True

def stop_market_long(symbol, stopPrice, quantity, reduceOnly=False):
    for i in range(3):
        try:
            if mode == "h":
                result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP_MARKET ,quantity=str(quantity), timeInForce=TimeInForce.GTC, positionSide="LONG", stopPrice=str(stopPrice), reduceOnly=reduceOnly)
            else:
                result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.STOP_MARKET ,quantity=str(quantity), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice), reduceOnly=reduceOnly)
            return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

        except Exception as err:
            print(f"{[symbol, stopPrice, quantity, reduceOnly]} {err} {extract_tb(exc_info()[2])}")

def stop_market_short(symbol, stopPrice, quantity, reduceOnly=False):
    for i in range(3):
        try:
            if mode == "h":
                result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, quantity=str(quantity), timeInForce=TimeInForce.GTC, positionSide="SHORT", stopPrice=str(stopPrice), reduceOnly=reduceOnly)
            else:
                result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.STOP_MARKET, quantity=str(quantity), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice), reduceOnly=reduceOnly)
            return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
        except Exception as err:
            print(f"{[symbol, stopPrice, quantity, reduceOnly]} {err} {extract_tb(exc_info()[2])}")
def get_price(symbol=None):
    if symbol:
        result = request_client.get_symbol_price_ticker(symbol=symbol)
        return float(ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))["price"])
    else:
        result = request_client.get_symbol_price_ticker()
        result = ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))
        res = {}

        for r in result:
            res[r["symbol"]] = float(r["price"])

        return res



def get_depth(symbol, limit=1000):
    result = request_client.get_order_book(symbol=symbol, limit=limit)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def close_long(symbol, quantity):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.MARKET, quantity=str(quantity), positionSide="LONG")
        return result

def close_short(symbol, quantity):
    if mode == "h":
        result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.MARKET, quantity=str(quantity), positionSide="SHORT")
        return result

def transferFromFutures(size):
    res = bot_spot.futuresTransfer(asset="USDT", amount=str(size), type=2)
    return res

def get_stop_orders(symbol):
    orders = get_open_orders(symbol)
    stop_orders = []

    for order in orders:
        if "STOP" in order["type"].upper():
            stop_orders.append(order)

    return stop_orders

def ping():
    stime = time.time()
    requests.get("https://fapi.binance.com/fapi/v1/ping")
    print(f"{int((time.time() - stime) * 1000)}ms")

def take_market_long(symbol, stopPrice, quantity, reduceOnly=False):
    result = request_client.post_order(symbol=symbol, side=OrderSide.SELL, ordertype=OrderType.TAKE_PROFIT_MARKET, quantity=str(quantity), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice), reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

def take_market_short(symbol, stopPrice, quantity, reduceOnly=False):
    result = request_client.post_order(symbol=symbol, side=OrderSide.BUY, ordertype=OrderType.TAKE_PROFIT_MARKET, quantity=str(quantity), timeInForce=TimeInForce.GTC, stopPrice=str(stopPrice), reduceOnly=reduceOnly)
    return ast.literal_eval(result.replace('"', "'").replace('false', "False").replace('true', "True"))

if __name__ == '__main__':
    print(get_orders("IOSTUSDT", True))