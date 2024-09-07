from connect_mysql import check_and_write_v4, standart_product_v2
from get_json import standart_wheels_from_json
from getcsv import standart_wheels_csv, standart_wheels_csv_v2
from main import get_new_pages_v2


def create_need_data(without_db=True, kolrad=True,
                     min_quantity=2):
    data = {}
    if not without_db:

        try:
            csv_data = standart_wheels_csv()
        except:
            csv_data = {}
            print("We don't get csv")
        try:
            json_data = standart_wheels_from_json()
        except:
            json_data = {}
            print("We don't get json")
        if kolrad:
            xml_data = check_and_write_v4()
        else:
            xml_data = {}
    else:
        try:
            csv_data = standart_wheels_csv_v2(without_db=True)[1]
        except:
            csv_data = {}
        try:
            json_data = standart_wheels_from_json(without_db=True)
        except:
            json_data = {}
        if kolrad:
            xml_data = standart_product_v2(get_new_pages_v2())
        else:
            xml_data = {}

    need_data = dict()
    # TODO it's need check
    if len(xml_data.keys()) > 0:
        data.update(xml_data)
        pre_csv_data = {key: value for key, value in csv_data.items()
                        if int(value[0][4]) >= min_quantity}
        pre_json_data = {k: v for k, v in json_data.items()
                         if int(v[0][4]) >= min_quantity}

        for ke, val in data.items():
            if pre_json_data.get(ke):
                pre_count_json = pre_json_data.get(ke)
                count_json = int(pre_count_json[0][4])
                del pre_json_data[ke]
            else:
                count_json = 0
            if pre_csv_data.get(ke):
                pre_count_csv = pre_csv_data.get(ke)
                count_csv = int(pre_count_csv[0][4])
                del pre_csv_data[ke]
            else:
                count_csv = 0

            in_stok = int(val[0][4]) + count_json + count_csv
            new_data = val[0].copy()
            del new_data[4]
            new_data.insert(4, in_stok)

            need_data.update({ke: (new_data, val[1], val[2], val[3], val[4])})

        need_data.update(pre_csv_data)
        need_data.update(pre_json_data)
    else:
        if len(json_data.keys()) > 0:
            data.update(json_data)
            pre_csv_data = {key: value for key, value in csv_data.items()
                            if int(value[0][4]) >= min_quantity}

            for ke, val in data.items():
                if pre_csv_data.get(ke):
                    pre_count_csv = pre_csv_data.get(ke)
                    count_csv = int(pre_count_csv[0][4])
                    del pre_csv_data[ke]
                else:
                    count_csv = 0

                in_stok = int(val[0][4]) + count_csv
                new_data = val[0].copy()
                del new_data[4]
                new_data.insert(4, in_stok)

                need_data.update({ke: (new_data, val[1], val[2], val[3], val[4])})

            need_data.update(pre_csv_data)
        else:
            need_data.update(csv_data)

    print('ALL_RIDE create_need_data ', len(need_data))

    return need_data
