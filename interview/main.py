import datetime
from flask import Flask, request, render_template
from gevent.pywsgi import WSGIServer

# create   the Flask app
app = Flask(__name__,
            # static_url_path='',
            static_folder='templates/static_files',
            template_folder='templates'
            )


@app.route('/', methods=['GET', 'POST'])
def example():
    date = datetime.date
    return render_template('create.html', date=date)#('index.html', date=date)


@app.route('/2', methods=['GET', 'POST'])
def index():
    date = datetime.date
    return render_template('index.html', date=date)#('index.html', date=date)

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Debug/Development
    # run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 9900), app)
    http_server.serve_forever()

# while True:
#     run_pending()
#     time.sleep(1)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
