
    
import csv

csv.field_size_limit(450000)

not_allowed = ['ГРМ', 'КПП', 'PEUGEOT', 'ГБЦ', 'RENAULT', 'CITROEN', 'OPEL', 'NISSAN',
               'INFINITI', 'FORD', 'CHRYSLER', 'CHEVROLET', 'BMW', 'РУП', 'SKODA']
some_fields = ['Новосибирск', 'Люберцы', 'Екатеринбург', 'Варшавка', 'Н.Новгород',
        'Дмитровка', 'Кетчерская', 'Хабаровская', 'Рябиновая', 'Машково', 'Ярославка',
               '!', 'Уфа', 'Ваш заказ', 'Пермь', 'Ижевск', 'Красногорск', 'Нефтекамск']

def read_csv_make_vendor():
    faxy = []
    with open('alliance _one_sheet.csv', 'r') as file:
        reader = csv.DictReader(file, delimiter=';')
        count = 0
        for row in reader:
            # if count < 159:
            pre_name = row['Все запчасти от А до Я']
            proxy = {key: value for key, value in row.items() if key not
                     in some_fields and (value != '' or value != 'Под заказ')}
            if pre_name:
                name = pre_name.split(' ')
                try:
                    if name[-2].isalpha() and name[-2].isupper() and name[-2] not in not_allowed:
                        vendor_name = ' '.join(name[-2:]).replace(')', '')

                        count += 1
                    elif name[-1].isalpha() and name[-1].isupper():
                        vendor_name = name[-1].replace(')', '')

                        count += 1
                    else:
                        vendor_name = 'Noname'

                        count += 1
                except:
                    vendor_name = 'Noname'

                    continue
                proxy['vendor'] = vendor_name
    
            faxy.append(proxy)
        print(11, len(faxy), count)

    return faxy


def rewrite_vendor():
    data = read_csv_make_vendor()
    fieldsnames = ['Код для заказа', 'Артикул товара', 'Артикул дополнительный', 'Все запчасти от А до Я',
                   'Розница', 'Опт 1', 'Опт 2', 'Опт 3', 'Опт 4', 'Общее наличие', 'vendor']
    with open('rewrite_allianse_all_in_one_sheet_csv.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fieldsnames)
        writer.writeheader()
        writer.writerows(data)
        print('ALL RIDE_rewrite_vendors')

rewrite_vendor()