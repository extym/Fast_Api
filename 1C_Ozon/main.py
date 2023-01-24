import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from lxml import etree
try:
    from xml.etree import cElementTree as ET
except ImportError:
    from xml.etree import ElementTree as ET


def get_cleaned_text(element):
    try:
        text = element.text
    except:
        text = u''
    if text is None:
        return u''
    return text.strip(u' ')


count = 0
#parser = ET.XMLParser()  #encoding="utf-8")
#root = ET.parse("offers0_1.xml", parser=parser)
parser = etree.XMLParser(ns_clean=True)
tree = etree.parse('offers0_1.xml', parser)
print('tree', type(tree))
root = tree.getroot()
print('root--', type(root))  # root[1][7])
for element in root[1][7]:
    el = element.findall('Предложение')
    print("1",el)
    print('2',element)
        # print('+++', el.text)
        # if el.attrib is not None:
        #     print('222', el.text)
    count += 1
#     print(type(el))
#     print('--', el)
print(count)

infile = open('offers0_1.xml')
outfile = open('out.xml', 'w')

replacements = {'Предложение':'mynum', 'Ид':'id'}

for line in infile:
    for src, target in replacements.items():
        lines = line.replace(src, target)
        outfile.write(lines)
infile.close()
outfile.close()


#convert xml to json
# import xmltodict
# import pprint
# import json
# with open('offers0_1.xml') as fd:
#     doc = xmltodict.parse(fd.read())   #, process_namespaces=True)
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json.dumps(doc))

#
# app = Flask(__name__)
#
# @app.route('/json', methods=['GET', 'POST'])
# def json_example():
#     request_data = request.get_json()
#     # if 'test' in request_data:
#     req = request.get_data()
#     print(req)
#     print(request_data)
#     return "OK"
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     # Debug/Development
#     # run app in debug mode on port 5000
#     # app.run(debug=True, host='0.0.0.0', port=5000)
#     # Production
#     http_server = WSGIServer(('', 8800), app)
#     http_server.serve_forever()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
