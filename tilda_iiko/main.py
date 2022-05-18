# import main Flask class and request object
from asyncore import read
from crypt import methods
import re
from flask import Flask, request
from cred import user_id, user_secret
import requests


class Biz:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.address = 'https://iiko.biz/api/0'

    def token(self):
        try:

            r = requests.get(
                self.address + '/auth/access_token?user_id=' + self.login + '&user_secret=' + self.password)
            r.text[1:-1]
            return r.text

        except requests.exceptions.ConnectTimeout:

             print("Не удалось получить токен " + "\n" + self.login)

i = Biz(user_id, user_secret)
token = i.token()
print('Token: ', token)


# create   the Flask app 
app = Flask(__name__)


@app.route('/api/0', methods=['POST'])
def query_example():
    payment = request.args.get("payment")
    print( '''<h2>The language value is: {}</h2>'''
           .format(payment))



@app.route('/', methods=['POST'])
def test():
    if request.get_data('test'):
        return 'test'

@app.route('/json', methods=['POST'])
def json_example():
    
    try: 
        request_data = request.get_json()
        customerName = request_data['customerName']
        customerPhone = request_data['phone']
        delivery = request_data['delivery']
        paymentsystem = request_data['paymentsystem']
        payment = request_data['payment']
        orderid = request_data['payment']['orderid']
        items = request_data['payment']['products']
        name = request_data['payment']['products'][0]
        amount = request_data['payment']['products'][0]
        code = request_data['payment']['products'][0]
        summ = request_data['payment']['products'][0]
    except LookupError:
        # if request_data == 'test':
        return 'test'
    # else:


    print(request_data)
    return 'JSON Object Example'


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
