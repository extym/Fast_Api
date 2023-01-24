import json
import datetime
import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer

def write_json(smth_json):
    with open('request.json', 'w') as file:
        json.dump(smth_json, file)

def write_smth(smth):
    f = open('test_txt.txt', 'w')
    f.write(smth)


def write_fake(smth):
    pass

data = '''
    {
    "order":
        {
     "shop": "Yandex",
     "businessId": 3675591,
     "id": "12345",
     "paymentType": "PREPAID",
     "itemsTotal": 5650,
     "delivery": false
     "items": {
     "sku": "1507145984637",
     "sku": "1507145987897"
            }
        }
    }
'''

def send_resp():
    r = requests.post('', data=data)


app = Flask(__name__)
#
@app.route('/json', methods=['GET', 'POST'])
def json_example():
    head = request.headers.get('X-Forwarded-For')
    ip_addr = request.environ.get('REMOTE_ADDR')  ## return
    #head = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)  ## return

    request_data = request.get_json()
    # if 'test' in request_data:
    write_json(request_data)
    data = json.dumps(request_data)
    write_smth(data)
    #print(data)

    return "OK"

@app.route('/order/accept', methods=['GET', 'POST'])
def close():
    data_req = request.get_json()
    # data_req = json.dumps(request_data)
    print('data_req', len(data_req), type(data_req))

    print('111', data_req)
    confirm_data = data_req["order"].get('fake')
    if confirm_data == True:
        write_fake(data_req)

    elif confirm_data == False:
        order = data_req["order"]
        shop_YM = data_req["order"]["businessId"]
        order_id = data_req["order"]["id"]
        payment_type = data_req["order"]["id"]
        payment_metod = data_req["order"]["id"]

        items = data_req["order"]["items"]  #list of dict's
        for row in items:
            shop_sku = row['shopSku']
            offerId = row['shopSku']
            count = row['count']


        #return items
        print(items)
    else:
        print(data_req)

    return 'OK'

@app.route('/reload', methods=['GET', 'POST'])
def reload():
    send_resp()
    return "OKi"

@app.route('/test', methods=['GET'])
def test():
    return "OK"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8800), app)
    http_server.serve_forever()
