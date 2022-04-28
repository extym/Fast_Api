import re
import time
import json
from datetime import datetime
import requests
import config as con
from parse import parse_data_time
from db import IdList, db, Config
from utils import *


URL = con.url
HEADERS = con.headers


res_str = ""


def logs(txt):
    with open("log.txt", "a+", encoding="utf-8") as file:
        file.write(txt + "\n")



class ConnectDb:
    """Working with the database"""

    def __init__(self):
        self.id_lst = self.__get_list_id()
        self.time_out = self.__get_timeout()
        self.key_word = self.__get_word_list()

    def set_timeout(self, new_time):
        try:
            new_time = int(new_time.strip())
            if new_time < 6 or new_time > 60:
                return False
            else:
                Config.update(timeout=new_time).where(Config.id == 1).execute()
                return True
        except Exception as e:
            if not type(e) is ValueError:
                db.rollback()
            logs(f"Error set timeout, error : {e}")
            return False

    def add_word_in_list(self, word):
        try:
            word = word.lower().stript()
            self.key_word.append(word)
            Config.update(key_word=self.key_word).where(Config.id == 1).execute()
            return True
        except Exception as e:
            logs(f"Error add new word, error : {e}")
            db.rollback()
            return False

    def del_key_word_in_list(self, word):
        try:
            word = word.lower().strip()
            if word in self.key_word:
                index_el = self.key_word.index(word)
                self.key_word.pop(index_el)
                Config.update(key_word=self.key_word).where(Config.id == 1).execute()
                return True
        except Exception as e:
            logs(f"Error delete word in list, error : {e}")
            db.rollback()
            return False

    def __get_word_list(self):
        try:
            word = Config.get(Config.id == 1)
            result_lst = [kw for kw in word.key_word]
            return result_lst
        except Exception as e:
            logs(f"Error get key word, error : {e}")
            db.rollback()

    def __get_timeout(self):
        try:
            timeout = Config.get(Config.id == 1).timeout
            return timeout
        except Exception as e:
            logs(f"Error get timeout, error : {e}")
            db.rollback()

    def to_update_lst_id(self, lst_id):
        if lst_id:
            self.id_lst += lst_id
            self.__update_list_id()

    def __get_list_id(self):
        try:
            list_id = IdList.get(IdList.id == 1)
            result_list = [i for i in list_id.id_list]
            if result_list: return result_list
            return []
        except Exception as e:
            db.rollback()
            logs(f"Error get id list, error : {e}")

    def __update_list_id(self):
        try:
            IdList.update(id_list=self.id_lst).where(IdList.id == 1).execute()
        except Exception as e:
            db.rollback()
            print(e)
            logs(f"Error update list id, error : {e}")

    def get_time_out(self):
        return self.time_out

    def set_pid(self, pid):
        try:
            Config.update(pid=pid).where(Config.id == 1).execute()
        except Exception as e:
            db.rollback()
            logs(f"Error set pid, error : {e}")

    def get_pid(self):
        try:
            pid = Config.get(Config.id == 1).pid
            return pid
        except Exception as e:
            db.rollback()
            logs(f"Error get pid, error : {e}")
            return False


class SendRequest:
    """Send request, return response"""
    def __init__(self, url, headers, data):
        self.resp = requests.post(url=url, headers=headers, data=json.dumps(data)).json()
        # global res_str
        # for title in range(len(self.resp["items"])):
        #     res_str += self.resp["items"][title]["subject"] + "::;"
        logs(f"[ {str(datetime.now())} ]: Send request page : {con.body['page']}")

    def get_state(self) -> bool:
        if self.resp["items"]:
            return True
        return False


class ProcessingData:
    """Data processing"""

    def __init__(self):
        self.result_data = []
        self.db = ConnectDb()
        self.id = self.db.id_lst
        self.word = self.db.key_word
        self.add_id_lst = []
        self.key_word = ["subject", "id", "price", "applicationFillingEndDate",
                         ["deliveryInfos", 0, "deliveryAddress", "formattedFullInfo"]]

    def processing_data(self, data):
        for count, d in enumerate(data["items"]):
            self.filter_data(d)

    def filter_data(self, data):
        for word in self.word:
            if data["subject"] is None:
                return None
            if re.findall(word, data["subject"].lower()):
                if data["id"] in self.id:
                    continue
                self.add_id_lst.append(data["id"])
                self.get_structure(data)

    def get_structure(self, data):
        structure_data = {}
        for key in self.key_word:
            if isinstance(key, list):
                structure_data["deliveryAddress"] = data[key[0]] #[key[1]][key[2]][key[3]]
                continue
            if key == "applicationFillingEndDate":
                structure_data["time"] = parse_data_time(data[key])
                continue
            structure_data[key] = data[key]
        structure_data["link"] = con.template_link.format(structure_data["id"])
        self.result_data.append(structure_data)

    def __del__(self):
        if self.add_id_lst:
            self.db.to_update_lst_id(self.add_id_lst)


class SendMsg():
    """Send Messages in telegram"""

    def __init__(self, data):
        self.data = data
        self.template_msg = con.template
        self.list_id = Config.get(Config.id == 1).id_admin
        self.send_msg()

    def send_msg(self):
        for item in self.data:
            msg = self.template_msg.format(item["subject"], item["link"], item["price"], item["deliveryAddress"], item["time"])
            for id_admin in self.list_id:
               # s = SendMessages()
               # s.send_mail(msg.encode("utf8"), id_admin)
                link = con.link_send_msg.format(id_admin, msg)
                r = requests.get(link)
                print(r)
                time.sleep(1)

