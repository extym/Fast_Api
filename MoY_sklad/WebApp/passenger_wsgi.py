# -*- coding: utf-8 -*-

######################## Django settings start #################################
# import os, sys
# sys.path.insert(0, '/home/b/b92955f9/b92955f9.beget.tech/ozon_ms')
# sys.path.insert(1, '/home/b/b92955f9/.local/lib/python3.6/site-packages')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'ozon_ms.settings'
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
######################## Django settings endss #################################

import sys, os
sys.path.append('/root/WebApp/flask_server')
#sys.path.append('/home/b/b92955f9/b92955f9.beget.tech/flask_server/') # указываем директорию с проектом
#sys.path.append('/home/b/b92955f9/.local/lib/python3.7/site-packages') # указываем директорию с библиотеками, куда поставили Flask
# sys.path.append('/home/b/b92955f9/b92955f9.beget.tech/flask')
from flask_server import app as application # когда Flask стартует, он ищет application. Если не указать 'as application', сайт не заработает
from werkzeug.debug import DebuggedApplication # Опционально: подключение модуля отладки
application.wsgi_app = DebuggedApplication(application.wsgi_app, False) # Опционально: включение модуля отадки
application.debug = False  # Опционально: True/False устанавливается по необходимости в отладке