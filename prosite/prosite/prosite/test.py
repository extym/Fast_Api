from spyne import Application, rpc, ServiceBase, Unicode, Iterable
from lxml import etree
from spyne.protocol.csv import Csv
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne import Integer


# app = Application([Soap], tns='Translator',
#                           in_protocol=Soap11(validator='lxml'),
#                          out_protocol=Soap11()
# application = WsgiApplication(app)
# if __name__ == '__main__':
#     from wsgiref.simple_server import make_server
#     server = make_server('0.0.0.0', 8000, application)
#     server.serve_forever()

class HelloWorldService(ServiceBase):
    @rpc(Unicode, Integer, _returns=Iterable(Unicode))
    def say_hello(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name
application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Csv()
)

