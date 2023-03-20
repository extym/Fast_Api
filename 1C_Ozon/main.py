import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer


app = Flask(__name__)

@app.route('/response', methods=['GET', 'POST'])
def test_example():
    request_data = request.get_json()
    req = request.get_data()
    print('req', req)
    print('request_data', request_data)
    return "OK"


if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 5500), app)
    http_server.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
