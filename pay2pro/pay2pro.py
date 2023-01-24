import json

from flask import Flask, request, redirect
import requests
import hashlib
secret_result = 'RPqJuSZAWdJu87YkrXjULhW4b20JHd'
failurl = 'https://api.pay2.pro/failurl'

app = Flask(__name__)

request_data = {
    'sp_salt': 5969408526,
    'sp_status': 'ok',
    'sp_payment_id': 511291497,
    'sp_redirect_url_type': 'payment_system',
    'sp_currency': 'RUB',
    'sp_redirect_url':
        {
            'url':
             'https://3ds.pay2.pro/payment/vAaNegrwXjR3kaMPGjYR'
         }
}


#
@app.route('/pay2pro', methods=['POST', 'GET'])
def json_get():
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
                    + sp_redirect_url_type + ';' + str(sp_salt) + ';' + sp_status + ';' + secret_result]
    signat = hashlib.sha256(sp_fool_resp.encode()).hexdigest()
    if sp_status == 'ok':
        return  redirect(target_payment_url, 302)  #,  Response=None) #redirect user?
    else:
        return redirect(failurl, 302)


@app.route('/get_form', methods=['POST', 'GET'])
def form_data():
    if request.method == 'POST':
        customer = request.form.get('customer')
        user_name = request.form.get('customer[firstname]')
        user_phone = request.form.get('customer[telephone]')
        amount = request.form.get('total_amount')
        user_contact_email = request.form.get('customer[email]')
        print(request.text())
        return '''<h2> ok <\h2>'''
    else:
        return '''
        <h2> Somthing wrong with request metod </h2>'''


    # # ll = []
    # # for key, value in request_data.items():
    # #     ll.append(item)
    # #     dic = dict(ll.sort())
    #
    #init_payment;RUB;511291497;https://3ds.pay2.pro/payment/vAaNegrwXjR3kaMPGjYR;payment_system;5969408526;ok;СЕКРЕТНЫЙКЛЮЧ

    # ll = ['RUB','511291497','payment_system','5969408526','ok','payment/vAaNegrwXjR3kaMPGjYR','RPqJuSZAWdJu87YkrXjULhW4b20JHd']
    # # [str(value) for key, value in request_data.items()]
    # #ll.append(secret_result)
    # s = ';'.join(ll)
    # print(s)
    #
    #
    # # sp_fool_resp = str(sp_salt) + ';' + sp_status + ';' + str(sp_redirect_url) + ';' \
    # #                + sp_status  + ';' + str(sp_payment_id)
    # signat = hashlib.sha256(s.encode()).hexdigest()
    # # if request_data['sp_status'] == 'ok':
    # #     pass

    #return signat

lst = []
print(json_get())