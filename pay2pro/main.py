from flask import Flask, request, render_template, redirect
from gevent.pywsgi import WSGIServer
import hashlib

failurl = 'https://api.pay2.pro/failurl'
secret_key = 'qKhfiV0YzILj25CxPPoHxGmnBRCqeT123'
# create   the Flask app
app = Flask(__name__,
            # static_url_path='',
            static_folder='templates/ctatic',
            template_folder='templates'
            )

@app.route('/pay2pro', methods=['GET', 'POST'])
def index():
    request_data = request.get_json()
    sp_status = request_data['sp_status']
    sp_salt = request_data['sp_salt']
    sp_payment_id = request_data['sp_payment_id']
    sp_redirect_url_type = request_data['sp_redirect_url_type']
    sp_currency = request_data['sp_currency']
    sp_redirect_url = request_data['sp_redirect_url']
    target_payment_url = sp_redirect_url['url']
    sp_sig = request_data['sp_sig']
    sp_fool_resp = [sp_currency + ';' + str(sp_payment_id) + ';' + str(sp_redirect_url) + ';'
                    + sp_redirect_url_type + ';' + str(sp_salt) + ';' + sp_status + ';' + secret_key]
    signat = hashlib.sha256(sp_fool_resp.encode()).hexdigest()
    if sp_status == 'ok':
        return  redirect(target_payment_url, 302)  #,  Response=None) #redirect user?
    else:
        return redirect(failurl, 302)
    #return "Hi, some!"  #render_template('smth.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.py')

@app.route('/form2', methods=['GET', 'POST'])
def xxx():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def vvvv():
    return '''
    <h3> HI, bro.</h3>'''''

if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8888), app)
    http_server.serve_forever()
