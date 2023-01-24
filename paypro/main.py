from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

# create   the Flask app
app = Flask(__name__,
            # static_url_path='',
            static_folder='templates/ctatic',
            template_folder='templates'
            )

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.py')

if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 8888), app)
    http_server.serve_forever()
