1. Скачать Python3 https://www.python.org/downloads/ (при установке должна быть нажата галочка add python.exe to PATH)
2. Запустить install.bat (в режиме администратора)
3. В файле config.py ввести данные API_key и API_secret для подключения к бинансу https://www.binance.com/ru/my/settings/api-management
4. Ввести желаемые данные в config.py:
4.1. mCur - стартовая валюта
4.2. mSum - стартовое количество валюты
4.3. mTimeout - время (количество прогонов) для проверки прибыли связки
4.4. mCommis - комиссия binance (стандартно 0,1% = 0,001)
4.5. mProfit - минимальная прибыль (там сложная формула, зависит от mSum)
4.6  mCount - количество отсортированных пар которые будут сканироваться
5. Запустить Start.bat