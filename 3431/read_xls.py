# import pandas as pd
#
# # read by default 1st sheet of an excel file
# dataframe1 = pd.read_excel('alliance (1).xls')
#
# print(dataframe1)

#
# import openpyxl
#
# # Define variable to load the dataframe
# dataframe = openpyxl.load_workbook("allianse_all_in_one_sheet.xlsx")
#
# # Define variable to read sheet
# dataframe1 = dataframe.active
#
# # Iterate the loop to read the cell values
# for row in range(11, 100):  #dataframe1.max_row):
#     for col in dataframe1.iter_cols(1, dataframe1.max_column):
#         if col[row].value is not None and col[row].value != 'Под заказ':
#             print(111, col[row], col[row].value)
#     print(dataframe1.max_column)
#     print(row)
    
    
import csv

# print(csv.field_size_limit())
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
                        # print(vendor_name)
                        count += 1
                    elif name[-1].isalpha() and name[-1].isupper():
                        vendor_name = name[-1].replace(')', '')
                        # print(vendor_name)
                        count += 1
                    else:
                        vendor_name = 'Noname'
                        # print(vendor_name)
                        count += 1
                except:
                    vendor_name = 'Noname'
                    # print(vendor_name)
                    continue
                proxy['vendor'] = vendor_name
    
            faxy.append(proxy)
        print(len(faxy), count)

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