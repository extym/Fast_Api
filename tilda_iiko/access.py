# import schedule
from schedule import every, repeat, run_pending
import time
import requests
from cred import user_id, user_secret
import datetime


class Biz:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.address = 'https://iiko.biz/api/0'

    def get_token(self):
        try:
            r = requests.get(
                self.address + '/auth/access_token?user_id=' + self.login + '&user_secret=' + self.password)
            r.text[1:-1]
            return r.text
        except requests.exceptions.ConnectTimeout:
            print("Не удалось получить токен " + "\n" + self.login)


i = Biz(user_id, user_secret)
token = i.get_token()
f = open('trap.py', 'w')
f.write('token = '+ token)
f.close()
# o = open('track','a') #open for append
# for line in open('file'):
#    line = line.replace('token ','newword')
#    o.write(line + 'n')
# o.close()
print('Token2: ', token)


# @repeat(every(899).seconds) #every(10).seconds) #for development
def job():
    i = Biz(user_id, user_secret)
    global token
    token = i.get_token()
    print(datetime.datetime.now(), 'token =', token)
    f = open('trap.py', 'w')
    f.write('token = ' + token)
    f.close()
    # return token


every(899).seconds.do(job)

while True:
    run_pending()
    time.sleep(1)

#
# def token():
#     return None
