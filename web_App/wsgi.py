from gevent.pywsgi import WSGIServer
from project import create_app
# from project import app


# def sensor():
#     """ Function for test purposes. """
#     print("Scheduler is alive!")
#
#
# # add scheduler
# from apscheduler.schedulers.gevent import GeventScheduler
#
# scheduler = GeventScheduler(daemon=True)
# sched.add_job(sensor, 'interval', minutes=60)
# sched.start()




# if __name__ == "__main__":
   #   app.run(host='0.0.0.0', port = '4567')




app = create_app()
http_server = WSGIServer(("0.0.0.0", 8000), app)
http_server.serve_forever()