import ast
import json
import os
import datetime
import time

try:
    os.mkdir("data")
except:
    pass

try:
    os.mkdir("data/logs")
except:
    pass

try:
    os.mkdir("data/klines")
except:
    pass

def saveCouples(couples):
    f = open("data/couples.txt", "w")
    f.write(str(couples))
    f.close()

def getCouples():
    settings = {}
    try:
        f = open("data/couples.txt")
        settings = ast.literal_eval(f.read())
        f.close()
    except:
        pass

    return settings

def saveSettings(settings):
    f = open("data/settings.txt", "w")
    f.write(str(settings))
    f.close()

def getSettings():
    settings = {}
    try:
        f = open("data/settings.txt")
        settings = ast.literal_eval(f.read())
        f.close()
    except:
        pass
    return settings

def saveKlines(symbol, klines, timeFrame):
    with open(f'data/klines/{symbol}_{timeFrame}.json', 'w', encoding='utf-8') as f:
        json.dump(klines, f, ensure_ascii=False, indent=4)

def getKlines(symbol, timeFrame):
    klines = []
    try:
        with open(f"data/klines/{symbol}_{timeFrame}.json") as f:
            klines.append(json.load(f))
        return klines[-1]
    except Exception as err:
        print(f"{symbol} {timeFrame} не удалось получить сохраненные свечи")
        return []

def saveHistory(history):
    f = open("data/history.txt", "a")
    f.write(str(history) + "\n")
    f.close()

def saveBalance(symbol, balance):
    pass
    # f = open("data/balances.txt", "a")
    # info = f"{str(datetime.datetime.today()).split('.')[0].replace(' ', ';')};{symbol};{balance}"
    # f.write(info + "\n")
    # f.close()

def saveOrder(order_info):
    pass
    # f = open("data/orders.txt", "a")
    # info = f"{order_info}"
    # f.write(info + "\n")
    # f.close()

def getBalance():
    balances = []

    balances_text = ""
    try:
        f = open("data/balances.txt")
        balances_text = f.read()
        f.close()
    except:
        pass

    if balances_text:
        for b in balances_text.split("\n"):
            if b:
                b_info = b.split(";")
                balances.append({
                    "symbols": b_info[2],
                    "date": b_info[1],
                    "time": b_info[0],
                    "balance": b_info[3],
                    "profit_fix": b_info[4]
                })

    return balances

title_log = f"{int(time.time() * 100000)}.txt"
def saveLog(log):
    f = open(f"data/logs/{title_log}", "a", encoding="utf-8")
    info = f"{log}"
    f.write(info + "\n")
    f.close()


# import time
# stime = time.time()
# print(getKlines("LINKUSDT", "3m"))
# print(time.time()-stime)
# print(getBalance())
# saveBalance("ETHUSDT", 10)