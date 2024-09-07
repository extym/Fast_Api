import datetime

from fast_bitrix24 import Bitrix
import base64


def convert_base64(file: str):
    with open(file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    return encoded_string


webhook = 'https://www.1000koles.ru/rest/4/c94acd8tqv0t1r2d/'

bx = Bitrix(webhook)
# result_cuts = bx.get_all('catalog.catalog.list')
#
# print(*result_cuts, sep='\n')

# result_list = bx.get_all('catalog.product.list', {
#     'select': [
#         'id',
#         'iblockId',
#         'name',
#     ],
#     'filter': {
#         'iblockId': 49
#     }
# })
# print(result_list[-1])
# result_prod = bx.get_all('catalog.product.get', {'id': 302841})
#
# print(111, *result_prod.items(), sep='\n')

def write_assortment():
    result_list = bx.get_all('catalog.product.list', {
        'select': [
            'id',
            'iblockId',
            'name',
        ],
        'filter': {
            'iblockId': 49
        }
    })
    for row in result_list.items():
        proxy = (

        )



def create_add_prod(data, type_prod: str = None):
    if type_prod == "tyres":
        description = data.get('description')
        name = data.get('name')
        in_stock = data.get('in_stock')
        width = data.get('width')
        articul = data.get('articul')
        quantity = data.get('quantity')
        brand = data.get('vendor')
        heigth = data.get('height')
        diameter = data.get('diameter')
        load_index = data.get('load_index')
        model_code = data.get('load_index')
        speed_index = data.get('load_index')
        season = data.get('season')
        tires_type = data.get('load_index')
        bolts = data.get('load_index')
        psd = data.get('load_index')
        et = data.get('load_index')
        hole = data.get('load_index')
        code_string = ''

        price = count_price()
        tyres_prod = {
            "active": "Y",
            "bundle": "N",
            "canBuyZero": "Y",
            "code": code_string,
            "createdBy": "1",
            "dateActiveFrom": None,
            "dateActiveTo": None,
            "dateCreate": datetime.datetime.now(),
            "detailText": description,
            "detailTextType": "text",
            "iblockId": '49',  # string?
            "iblockSectionId": "11",
            "length": "123",
            "measure": "5",
            "modifiedBy": "1",
            "name": name,  # urlDecode ?
            "previewText": None,
            "previewTextType": "text",
            "purchasingCurrency": "RUB",
            "purchasingPrice": price,  # string
            "quantity": quantity,  # string
            "quantityReserved": "0",
            "quantityTrace": "N",
            "sort": "500",
            "subscribe": "Y",
            "vatId": None,
            "vatIncluded": "N",
            "weight": None,
            "width": width,  # string
            "xmlId": None,  # check - is it nessesety?
            'property574': {'value': '9630.00'},
            'property575': {'value': '9630.00'},
            'property590': {'value': articul},  # артикул '1033939'
            'property601': {'value': in_stock},  # check it
            'property607': {'value': quantity},  # default 218 ?
            'property737': {'value': brand},  # model ? 'Hankook Laufenn'
            'property738': {'value': heigth},
            'property739': {'value': model_code},
            'property740': {'value': diameter},
            'property741': {'value': load_index},
            'property742': {'value': speed_index},
            'property743': {'value': season},
            'property744': {'value': tires_type},  # легковая
            'property754': {'value': bolts},
            'property755': {'value': psd},  # расстояние между болтами
            'property756': {'value': et},  # вылет
            'property757': {'value': hole},
            "height": "1",
            "property98": [
                {"value": {
                    "fileData": [
                        "previewSmall.png",
                        "iVBORw0KGgoAAAANSUhEUgAAAEUAAABFCAYAAAAcjSspAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAqZSURBVHhe7VxbbBxXGf7W6\/U6vjeOYztJkzSOG3KRk4CKUFEV1AdeEChcVO4XNVJBFUgVlMtDIkDlAQRI3MVDVakVKioUBA9IPLUqJeIWaEJEE4hShSp1LnYudnxde3f5vjNz7PHszO7s7KwvyJ9yMuN\/ds7lm\/\/8lzNnN1UksIIosPVCAcjz2JBySrrBvbhCWDZSZueB8WlgKgfMzAFzeWCeZASCPRIxjWmgOeOUzg1AS5N7vc6oKykTs8DoHeAOj3kSIC3gP\/OfOerUnnhgOuT2Sgf1UBql 0XQpjZgY6tzvR5InBTVdmWMZEw454YId BBBFQD1afO2inX1QJs6QSyJCpJJEaKNGH4NnBjctE2CLUSEQTbYx3nWdqywNau5KZXIqRcG3e0w5JRDyLCYLVHD0V2Z2d37e3XRMo0jebFEcdzpJeZDD8MOSwiZ tdQE 7eyEGYpMi7dB0ydBDCCtJiBcajbxaezMw0OMKq0QsUi5cp2ulR5HbXC1k CGNUd\/29AJNja4wIqom5dUrfBKMMRpEiCtbrbBacy JqcYIRyZFLlCE6NMiZK1A\/VWguItTSYY4CiIPzxDC41oiRNAUkt17jQ5hko4hCiIN8ZzVkNU X0JgiblwFcgx3aiEiqTI5Ur91pqG CFilEudJzGVUHao15W3zKxdDfFDxGgo\/7nm\/B2GUFKU1Q7fIrv8hCr7f4E0XkGn4qwwhHofGVab2YahyGsFSys\/Ww4ptqKqVEyDcpH8Q fR\/F90pNTvMrbDeqShbcFrN4GkKMN9Q1riRqtBECGZmZtou3aKxDShsbWA RYmHsVgdlJkbTx7CIUUK2Uw1XDqHHs2hyZW1NzQiGI2mWwuxdghd1cHJnf1liVGmfYGZte7N7sCDwJJOXO5ci4zzzHs sNxtF\/8DQMAJhv3H6Jp9\/k8U7NbfXEKV7o jZGOB9B44w4yH30ccx2tGOzZikyGlamX9rOxIdVjHfk8Tj\/9eWSYpIZBH1Ngp1RAKYEXJcqjbFdcRLEjhTRz9qZOlg7e0MLa2pyS0goQB5pS4WdUkOWQneaKrLzYxs zFFrYow283qrC85oK67D1VYDGp6mjGeFHiab8k1oSJf2Xpuw8 QQ6L\/2emtIF3HeA08HV1wI1pmM\/dfMzzt8uhjktNTXTtyeQeeQE5qkpA939yDZmcKmQwon5RpCqWJhmOZbO44jmzFwBp3\/6aFlNsZBt0RTSmozFEk0ZoQsWQ1G0pCxkV5qpl5pOT74HeOYjwFNHGQW YOxJEG6yiFK1H7eMyNBVCWmLvKwXJaTIliSCAh BbMXBDwAHSMzB9wEbd1DuXvdBHTGF7ccqvLeMXwiF7lX4L09rsUCK4pIcx1GzllhIW1TXfZ8A3vwh4C08bh5g685lP9QnXdKCVazCe8s4m7KQtoxwWlsskHKDQrFWF SmyDonOF2wISoAfQxkulhaYxaad xsCFHDCtC4b3pIWTC0SvrswkwUlDW0eeYGmx4AdlBDhOO9JjQePvI9jA59EGk Fr hdaxCAhAv83TJEQ2tYLw479u\/xYnNjKZorURTp254gox\/9XXg8EMkzpX5oaBhjD7EW QaNDf8cnVWcr1d88tjwCqC3k8JhhS9tNKDSsye JFiMylqg6x4kELoMfUw1vnBJ4Fv01Op6Hx3H30l4w6\/fO9Wejeq6vdpp7zygzTkVlurhKbQOBXcnOs\/vcpMnBARIVV 8TvAyz8CXvouI6V\/BbsIE1pyim1hZHwPgwYVne\/pB 7eWCoXKXrRs4XXvPKhux3tigGNf8YNyA0p0 H2Lz7USp4VX30VuP5vpqXMdaZvhzfk9YkWIkvFDy0SB30 JiEW9nZDyqxISZoVE6dwynz4KeD9PwQeehIYfDsH5F73I6gDEgW5RH026PM1uk\/xb95Z6w\/ZrGWB2gnqtwajRQ4\/tHaoLQp 5CgLkksWkxjLsYnV5JLPvuH0tRptqcolf2uInS1g G3fwOjeo0gzASpxyZO09rYTljxNETtIr1yP1IbeS QckZJCXq\/GJVvo9kGaNkNKlKUCP6oi5fIr7PgchhsGMNrYjfQtHylaY lm PXZdy5qgPZcPP0yQ81x4Avvcua4lf\/sJOtktvTldy\/KtfXgl38BztL1cyBxSRmgzTbTR3FKXbHtML3IW5k5dzseyQ89eblfeRF5FhWd7 NxO \/Z5ZMfoJfZRm\/jlev8sFwyR1YDxIUhpS4r9VbtXv boymXeRwfdVsMQJg3WUbvI4gLh5Qqpk1kaEpMMe1 9lPA848CP38YeO2PwXGKENQHyYLmdDXzvEqIi\/qRUqB9aWkHvsKA7bE\/AV88Cxw6yqfsXvdC7StN90NaEvT2SrarDsTIXi9oSmJrKJWgdtSyH9oW8NeLwMd vFg \/hPgd5x254dL5c\/92TG4CcKuPzbZhFCGe miZMJ47hGWY8AFeo2glTfZh356sBPvBb5Ej6JynFqlMF87\/vxyhfOyKwlD77gWpo W uvJCXr3AX172RAHHtSQpsm9JGAPc\/eh7U7RubzMjk2l8sP3JGJU\/bAbkAwp2rtRV015x2PAkceZxO2nVrgyP6r1PglD41fiLRhSzEo21aYuxORpFGV0GbyZfCLMfgXJJQszqIGfD6u8MpTzdDQ754YUWVwZmESRpvGYuAV8jer TWrI1xlYvfIL6qh73QuNJWiBSD0N0go9vbkADVLkFYMYqwzt7muOheVIbeoz72QMTZUROcyfYZhuOsrcZ7IFo7lM4Hsfs5jRRaNqB6WDWTjliXYRL5FP8j92u1Mv4NwOW7meLqdctcuRMrD7 PyEBQq0tdu8uUwazR10b4xXsp3OUkJYG3KBSgonSKiK9oBIlqXGlcgpkwHQ6phfbtipDhr3Rq18u1ggRaGCSK7ZrgT16e\/PsjwDXGcsEjZNpQlSU2 RLEwuhMmrhGx8TxApgjbkxl5bMR3izbN8eqaDnqpPPw c RXV 7 Fl3wszmt0sV4yrVCWtJKpVOXLUpIMUOLQ4zeDZw8A7zEKHRsivPa8y7y2K Bh3\/LbPZByl2ZiwYSMjZ9B evXcalW1eXkrkMkJZoedeLkh6ImNi2xRg93txIMz7GnOcfn1sspxjRXmVEGzBmEaMmdUwG0QagcTbTbHhfrgslveinPVSVUbSlIU8DmKOJz9HD5JgR3z8IPEgv1Mqbi7xW5FQyRxbMUgsdN0qXh9QEtUllcgrtxTQOdvZie5ZG2choNOOWKZZptVceGp 0RPv4\/VhwyV7UtJNJlAYwWmknE7Lav1J6X7Wo204mYX3PWwC0vHGOWbu0JaanW7VQkNxHM9HL2RqEUMumOEhWWflY0k9yJaFMYAO1NIwQoay530xPpE1ysb3RKoMeroaib3WUQ1lSBO0e1DpD3Vf86wwRomnzpj5XUAYVSRH29jt2Za1qjDWsgyQkyheiIpEi7BMxPK41jbGE6Ps CuejINT7hGH9m2EhWP8OYQhW 7dNtQFqN6dMHMQmRVj\/XnIZrH DPQTq1PpvHYRAta3\/KkYZmN9PITlaU7YZt HFHnUaQJTpkNsrHdRDEaH7le5rf8 a v2UMKz\/0k4VsFNBHkyaIC9mX WsDID\/AZreGI9CxIpzAAAAAElFTkSuQmCC\n"
                    ]}
                }
            ]
        }

        create_result = bx.call('catalog.product.add', {"fields": tyres_prod})

    elif type_prod == "wheels":
        description = data.get('description')
        name = data.get('name')
        in_stock = data.get('in_stock')
        width = data.get('width')
        articul = data.get('articul')
        quantity = data.get('quantity')
        brand = data.get('vendor')
        heigth = data.get('height')
        diameter = data.get('diameter')
        load_index = data.get('load_index')
        model_code = data.get('load_index')
        speed_index = data.get('load_index')
        season = data.get('season')
        tires_type = data.get('load_index')
        bolts = data.get('load_index')
        psd = data.get('load_index')
        et = data.get('load_index')
        hole = data.get('load_index')
        code_string = ''

        price = count_price()
        tyres_prod = {
            "active": "Y",
            "bundle": "N",
            "canBuyZero": "Y",
            "code": code_string,
            "createdBy": "1",
            "dateActiveFrom": None,
            "dateActiveTo": None,
            "dateCreate": datetime.datetime.now(),
            "detailText": description,
            "detailTextType": "text",
            "iblockId": '49',  # string?
            "iblockSectionId": "10445",
            "length": "123",
            "measure": "5",
            "modifiedBy": "1",
            "name": name,  # urlDecode ?
            "previewText": None,
            "previewTextType": "text",
            "purchasingCurrency": "RUB",
            "purchasingPrice": price,  # string
            "quantity": quantity,  # string
            "quantityReserved": "0",
            "quantityTrace": "N",
            "sort": "500",
            "subscribe": "Y",
            "vatId": None,
            "vatIncluded": "N",
            "weight": None,
            "width": width,  # string
            "xmlId": None,  # check - is it nessesety?
            'property574': {'value': '9630.00'},
            'property575': {'value': '9630.00'},
            'property590': {'value': articul},  # артикул '1033939'
            'property601': {'value': in_stock},  # check it
            'property607': {'value': quantity},
            'property737': {'value': brand},  # model ? 'Hankook Laufenn'
            'property738': {'value': heigth},
            'property739': {'value': model_code},
            'property740': {'value': diameter},
            'property741': {'value': load_index},
            'property742': {'value': speed_index},
            'property743': {'value': season},
            'property744': {'value': tires_type},  # легковая
            'property754': {'value': bolts},
            'property755': {'value': psd},  # расстояние между болтами
            'property756': {'value': et},  # вылет
            'property757': {'value': hole},
            "height": "1",
            "property98": [
                {"value": {
                    "fileData": [
                        "previewSmall.png",
                        "iVBORw0KGgoAAAANSUhEUgAAAEUAAABFCAYAAAAcjSspAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAqZSURBVHhe7VxbbBxXGf7W6\/U6vjeOYztJkzSOG3KRk4CKUFEV1AdeEChcVO4XNVJBFUgVlMtDIkDlAQRI3MVDVakVKioUBA9IPLUqJeIWaEJEE4hShSp1LnYudnxde3f5vjNz7PHszO7s7KwvyJ9yMuN\/ds7lm\/\/8lzNnN1UksIIosPVCAcjz2JBySrrBvbhCWDZSZueB8WlgKgfMzAFzeWCeZASCPRIxjWmgOeOUzg1AS5N7vc6oKykTs8DoHeAOj3kSIC3gP\/OfOerUnnhgOuT2Sgf1UBql 0XQpjZgY6tzvR5InBTVdmWMZEw454YId BBBFQD1afO2inX1QJs6QSyJCpJJEaKNGH4NnBjctE2CLUSEQTbYx3nWdqywNau5KZXIqRcG3e0w5JRDyLCYLVHD0V2Z2d37e3XRMo0jebFEcdzpJeZDD8MOSwiZ tdQE 7eyEGYpMi7dB0ydBDCCtJiBcajbxaezMw0OMKq0QsUi5cp2ulR5HbXC1k CGNUd\/29AJNja4wIqom5dUrfBKMMRpEiCtbrbBacy JqcYIRyZFLlCE6NMiZK1A\/VWguItTSYY4CiIPzxDC41oiRNAUkt17jQ5hko4hCiIN8ZzVkNU X0JgiblwFcgx3aiEiqTI5Ur91pqG CFilEudJzGVUHao15W3zKxdDfFDxGgo\/7nm\/B2GUFKU1Q7fIrv8hCr7f4E0XkGn4qwwhHofGVab2YahyGsFSys\/Ww4ptqKqVEyDcpH8Q fR\/F90pNTvMrbDeqShbcFrN4GkKMN9Q1riRqtBECGZmZtou3aKxDShsbWA RYmHsVgdlJkbTx7CIUUK2Uw1XDqHHs2hyZW1NzQiGI2mWwuxdghd1cHJnf1liVGmfYGZte7N7sCDwJJOXO5ci4zzzHs sNxtF\/8DQMAJhv3H6Jp9\/k8U7NbfXEKV7o jZGOB9B44w4yH30ccx2tGOzZikyGlamX9rOxIdVjHfk8Tj\/9eWSYpIZBH1Ngp1RAKYEXJcqjbFdcRLEjhTRz9qZOlg7e0MLa2pyS0goQB5pS4WdUkOWQneaKrLzYxs zFFrYow283qrC85oK67D1VYDGp6mjGeFHiab8k1oSJf2Xpuw8 QQ6L\/2emtIF3HeA08HV1wI1pmM\/dfMzzt8uhjktNTXTtyeQeeQE5qkpA939yDZmcKmQwon5RpCqWJhmOZbO44jmzFwBp3\/6aFlNsZBt0RTSmozFEk0ZoQsWQ1G0pCxkV5qpl5pOT74HeOYjwFNHGQW YOxJEG6yiFK1H7eMyNBVCWmLvKwXJaTIliSCAh BbMXBDwAHSMzB9wEbd1DuXvdBHTGF7ccqvLeMXwiF7lX4L09rsUCK4pIcx1GzllhIW1TXfZ8A3vwh4C08bh5g685lP9QnXdKCVazCe8s4m7KQtoxwWlsskHKDQrFWF SmyDonOF2wISoAfQxkulhaYxaad xsCFHDCtC4b3pIWTC0SvrswkwUlDW0eeYGmx4AdlBDhOO9JjQePvI9jA59EGk Fr hdaxCAhAv83TJEQ2tYLw479u\/xYnNjKZorURTp254gox\/9XXg8EMkzpX5oaBhjD7EW QaNDf8cnVWcr1d88tjwCqC3k8JhhS9tNKDSsye JFiMylqg6x4kELoMfUw1vnBJ4Fv01Op6Hx3H30l4w6\/fO9Wejeq6vdpp7zygzTkVlurhKbQOBXcnOs\/vcpMnBARIVV 8TvAyz8CXvouI6V\/BbsIE1pyim1hZHwPgwYVne\/pB 7eWCoXKXrRs4XXvPKhux3tigGNf8YNyA0p0 H2Lz7USp4VX30VuP5vpqXMdaZvhzfk9YkWIkvFDy0SB30 JiEW9nZDyqxISZoVE6dwynz4KeD9PwQeehIYfDsH5F73I6gDEgW5RH026PM1uk\/xb95Z6w\/ZrGWB2gnqtwajRQ4\/tHaoLQp 5CgLkksWkxjLsYnV5JLPvuH0tRptqcolf2uInS1g G3fwOjeo0gzASpxyZO09rYTljxNETtIr1yP1IbeS QckZJCXq\/GJVvo9kGaNkNKlKUCP6oi5fIr7PgchhsGMNrYjfQtHylaY lm PXZdy5qgPZcPP0yQ81x4Avvcua4lf\/sJOtktvTldy\/KtfXgl38BztL1cyBxSRmgzTbTR3FKXbHtML3IW5k5dzseyQ89eblfeRF5FhWd7 NxO \/Z5ZMfoJfZRm\/jlev8sFwyR1YDxIUhpS4r9VbtXv boymXeRwfdVsMQJg3WUbvI4gLh5Qqpk1kaEpMMe1 9lPA848CP38YeO2PwXGKENQHyYLmdDXzvEqIi\/qRUqB9aWkHvsKA7bE\/AV88Cxw6yqfsXvdC7StN90NaEvT2SrarDsTIXi9oSmJrKJWgdtSyH9oW8NeLwMd vFg \/hPgd5x254dL5c\/92TG4CcKuPzbZhFCGe miZMJ47hGWY8AFeo2glTfZh356sBPvBb5Ej6JynFqlMF87\/vxyhfOyKwlD77gWpo W uvJCXr3AX172RAHHtSQpsm9JGAPc\/eh7U7RubzMjk2l8sP3JGJU\/bAbkAwp2rtRV015x2PAkceZxO2nVrgyP6r1PglD41fiLRhSzEo21aYuxORpFGV0GbyZfCLMfgXJJQszqIGfD6u8MpTzdDQ754YUWVwZmESRpvGYuAV8jer TWrI1xlYvfIL6qh73QuNJWiBSD0N0go9vbkADVLkFYMYqwzt7muOheVIbeoz72QMTZUROcyfYZhuOsrcZ7IFo7lM4Hsfs5jRRaNqB6WDWTjliXYRL5FP8j92u1Mv4NwOW7meLqdctcuRMrD7 PyEBQq0tdu8uUwazR10b4xXsp3OUkJYG3KBSgonSKiK9oBIlqXGlcgpkwHQ6phfbtipDhr3Rq18u1ggRaGCSK7ZrgT16e\/PsjwDXGcsEjZNpQlSU2 RLEwuhMmrhGx8TxApgjbkxl5bMR3izbN8eqaDnqpPPw c RXV 7 Fl3wszmt0sV4yrVCWtJKpVOXLUpIMUOLQ4zeDZw8A7zEKHRsivPa8y7y2K Bh3\/LbPZByl2ZiwYSMjZ9B evXcalW1eXkrkMkJZoedeLkh6ImNi2xRg93txIMz7GnOcfn1sspxjRXmVEGzBmEaMmdUwG0QagcTbTbHhfrgslveinPVSVUbSlIU8DmKOJz9HD5JgR3z8IPEgv1Mqbi7xW5FQyRxbMUgsdN0qXh9QEtUllcgrtxTQOdvZie5ZG2choNOOWKZZptVceGp 0RPv4\/VhwyV7UtJNJlAYwWmknE7Lav1J6X7Wo204mYX3PWwC0vHGOWbu0JaanW7VQkNxHM9HL2RqEUMumOEhWWflY0k9yJaFMYAO1NIwQoay530xPpE1ysb3RKoMeroaib3WUQ1lSBO0e1DpD3Vf86wwRomnzpj5XUAYVSRH29jt2Za1qjDWsgyQkyheiIpEi7BMxPK41jbGE6Ps CuejINT7hGH9m2EhWP8OYQhW 7dNtQFqN6dMHMQmRVj\/XnIZrH DPQTq1PpvHYRAta3\/KkYZmN9PITlaU7YZt HFHnUaQJTpkNsrHdRDEaH7le5rf8 a v2UMKz\/0k4VsFNBHkyaIC9mX WsDID\/AZreGI9CxIpzAAAAAElFTkSuQmCC\n"
                    ]}
                }
            ]
        }

        create_result = bx.call('catalog.product.add', {"fields": tyres_prod})

    print(55555, create_result)


def update_prod(product=None):
    '''
    product = {vendor.strip() + product_code:
            {
                "category_id": category_id,
                "name": name,
                "description": description,
                "price": price,
                "in_stock": in_stock,
                "enabled": enabled,
                "product_code": product_code,
                "vendor": vendor,
                "meta_d": meta_d,
                "meta_k": meta_k,
                "params": params,
                "koeff": koeff,
                "meta_h1": meta_h1,
                "provider": provider,
                "category": category,
                'diameter': prod.get('diameter'),
                'width': prod.get('width'),
                'profile': prod.get('height')
            }
        }
    :param product:
    :return:
    '''
    id = 302841
    quantity = 111
    tyres_prod = {
        "active": "Y",
        'canBuyZero': 'N',
        'name': '225/65R17 102H G Fit EQ+ LK41 TL',
        "iblockId": '49',  # string?
        "iblockSectionId": 10445,
        "quantity": quantity,
        'property574': '9700.00',
        'property575': '9700.00'
    }
    update_result = bx.call('catalog.product.update', {
        "id": id,
        "fields": tyres_prod})
    print(5555555555555555555555555, *update_result.items(), sep='\n')
    for key in update_result.keys():
        print(f'row[{key}]: row.get("{key}").get("value", row.get("{key}")')


def update_price_prod(product=None):
    '''
    product = {vendor.strip() + product_code:
            {
                "category_id": category_id,
                "name": name,
                "description": description,
                "price": price,
                "in_stock": in_stock,
                "enabled": enabled,
                "product_code": product_code,
                "vendor": vendor,
                "meta_d": meta_d,
                "meta_k": meta_k,
                "params": params,
                "koeff": koeff,
                "meta_h1": meta_h1,
                "provider": provider,
                "category": category,
                'diameter': prod.get('diameter'),
                'width': prod.get('width'),
                'profile': prod.get('height')
            }
        }
    :param product:
    :return:
    '''
    id = 302841
    price_id = 19495
    tyres_prod = {
        "catalogGroupId": 1,
        "currency": "RUB",
        "price": 9100,
        "productId": id
    }
    update_result = bx.call('catalog.price.update', {"id": price_id, "fields": tyres_prod})
    print(77777777777777, *update_result.items(), sep='\n')


# print(bx.get_all('catalog.price.list', {
#     'select': [
#         'id',
#         'productId',
#         'catalogGroupId',
#     ],
#     'filter': {
#         'iblockId': 49
#     }
# }))

# print(bx.call('catalog.price.get',
#               {"id": 19495}))


update_prod()
# update_price_prod()