from gevent.pywsgi import WSGIServer
from project import create_app
# from project import app




# if __name__ == "__main__":
   #   app.run(host='0.0.0.0', port = '4567')




app = create_app()
http_server = WSGIServer(("0.0.0.0", 8000), app)
http_server.serve_forever()