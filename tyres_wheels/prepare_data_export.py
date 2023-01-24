import json
from connect import write
# data = {'name': 'MAK Highlands 7,0x17 5/114,3 ET40 d-60,1 Black Mirror (F7070HIBM40FP2X)', 'currency': 'rur', 'category': 5, 'vendor': 'MAK', 'vendorCode': '00092877', 'picture': 'https://b2b.kolrad.ru/dbpics/66369094.png', 'sale': False, 'discounted': False, 'params': [{'name': 'D (размер обода)', 'value': 'x17'}, {'name': 'Страна производства', 'value': 'Италия'}, {'name': 'Цвет для поиска', 'value': 'Чёрный глянцевый с полированной лицевой частью'}, {'name': 'Модель', 'value': 'Highlands'}, {'name': 'Цвет', 'value': 'Black Mirror'}, {'name': 'DIA', 'value': 'd-60,1'}, {'name': 'ET', 'value': 'ET40'}, {'name': 'LZ (ширина обода)', 'value': '7,0'}, {'name': 'PCD', 'value': '5/114,3'}, {}], 'price': {'rrc': 17540.0, 'regular': 15660.0, 'b2b': 15660.0}, 'stocks': [{}], 'description': '<p>Если вы хотите придать своему автомобилю внешность агрессивного, выразительного спорт кара или элегантность респектабельной машины представительского класса, тогда предлагаем вам купить диски MAK. Колесные аксессуары этой марки известны во всем мире и являются эталоном высокого качества, долговечности, а также безупречного стиля.Производителем литых дисков MAK является итальянская компания Mak Wheels, основанная в 1990 году путем слияния двух мощных производственных концернов, работавших в сфере изготовления авто деталей не одно десятилетие.Компания Magri, являющая одним из совладельцев компании Mak Wheels, занималась продажей автомобильных шин. А вторым основателем этого бренда стал Cervati - итальянский промышленный концерн, работающий в области производства деталей из алюминия, имеющий собственные литейные цеха и основанный в 30-х годах XX века.&nbsp;При производстве литых дисков MAK основной упор делается на внедрение инновационных технологий, которые призваны увеличить их прочность и срок эксплуатации, а также оригинальный дизайн, подчеркивающий лаконичную внешность любого транспортного средства.</p><p>MAK - диски, владельцы которых ценят отменное итальянское качество, их отличные эксплуатационные свойства, легкость, прочность и привлекательный дизайн. Тем более что производитель предлагает диски самых разных стилей, начиная от изящных и элегантных, заканчивая агрессивными, спортивными моделями.</p><p>Поэтому диски MAK купить - значит стать обладателем важной детали ходовой, благодаря которой вы сможете улучшить маневренность и управляемость вашего транспортного средства.</p><p>MAK - это диски литые, обладающие еще одним немаловажным достоинством, таким как коррозийная устойчивость. Они не боятся резких перепадов температуры, устойчивы к постоянному воздействию влаги, а также различных агрессивных веществ.</p><p>Мы предоставляем покупателю пятилетнюю гарантию на диски MAK.</p><p>Сайт производителя <a href=&apos;https://www.makwheels.it/&apos;>https://www.makwheels.it/</a></p><p>Конфигуратор&nbsp; <a href=&apos;https://www.makwheels.it/it-it/car-configurator.aspx&apos;>https://www.makwheels.it/it-it/car-configurator.aspx</a></p>'}

categories = { 'iFree' : 628, 'Carwel' : 1969,  'KHOMEN' : 1968,  'КиК' : 1782 , 'Скад'  : 1926}
list_vendors = ['iFree', 'Carwel', 'KHOMEN', 'КиК', 'Скад']   #, '\\u041a\\u0438\\u041a', "\u041a\u0438\u041a", '\u0421\u043a\u0430\u0434'] #list(categories.keys())


def is_in_stocks(stock):
    quantity = 0
    for i in range(len(stock) - 1):
        try:
            if stock[i]['name'] == 'Скл Видное':
                if stock[i]['quantity'].isdigit():
                    quantity = int(stock[i]['quantity'])
                elif stock[i]['quantity'][1:].isdigit():
                    quantity = int(stock[i]['quantity'][1:])
            elif stock[i]['name'] == 'Поставщики':
                continue
            else:
                continue
        except KeyError as er:
            #write("Smth went wrong KeyError from is_in_stocks: {}".format(er))
            print("Smth went wrong KeyError from is_in_stocks: {}".format(er))
            #quantity = 0
            continue

    return quantity


def get_need_data():
    need_data = []
    for line in open('data_product.json', 'r'):
        l = line.replace('}"" {', ',') #[1:-1]
        our_data = json.loads(l)
        print(type(our_data))
        try:
            for lin in our_data:
                quantity = lin.get('in_stock')
                if quantity is None:
                    quantity = is_in_stocks(lin['stocks'])
                category = lin['category']
                price = lin.get('price_b2b')
                if price is None:
                    price = lin['price']['b2b']
                if lin['vendor'] in list_vendors and int(quantity) >= 4 \
                        and category in [1, 4, 5, 7]\
                        and price >= 7200:
                    lin['count'] = quantity
                    need_data.append(lin)

        except KeyError as err:
            write("Smth went wrong KeyError from get_need_data: {}".format(err))
            print("Something went wrong KeyError from get_need_data: {}".format(err))
            print('from_prepare_data_lin', lin)
            continue
        except TypeError as error:
            write("Smth went wrong KeyError from get_need_data: {}".format(error))
            print("Smth went wrong TypeError from get_need_data: {}".format(error))
            continue

    print('need_data2 - ', len(need_data), type(need_data))
    # with open("need_data.json", "w") as write_file:
    #     json.dump(need_data, write_file) # encode dict into JSON

    return need_data

#get_need_data()