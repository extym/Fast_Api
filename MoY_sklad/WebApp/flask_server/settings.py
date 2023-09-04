"""
Настройки
"""

TEST_MODE = 0 # 1 - skip login, 0 - with authentication
LOCAL_MODE = 1 # 1 - local, 0 - hosting
LOGGING = 0

if LOCAL_MODE:
    ROOT_DIR = ""
    PUBLIC_DIR = "../public_html/"
else:
    ROOT_DIR = "/root/WebApp/flask_server/"
    PUBLIC_DIR = "/root/WebApp/public_html/"

LABEL_DIR = "labels/"
ACT_DIR = 'acts/'

LOGIN = "16_58_admin"
PASSW = "admin58_16"

#URL = "http://185.41.161.50/"
URL = "http://127.0.0.1:4567"

LOG_FILE = "log.txt"
ORDERS_LOG_FILE = "orders_log.txt"
ACTS_LOG_FILE = "acts_log.txt"

######################### DB ###############################
#MYSQL_HOST = "185.41.161.50"
MYSQL_HOST = "localhost"
if not LOCAL_MODE:
    MYSQL_HOST = "localhost"
MYSQL_USER = "root2"
MYSQL_PASW = "AscOj7Cm"
# MYSQL_USER = "root"
# MYSQL_PASW = "toor_Pass1!"

MYSQL_DATABASE = "database_name"
DB_DICTS = [
    'organization',
    'counterparty',
    'store'
]
############################################################

################# Настройки HTTP REQUEST ###################
# Число попыток request при неуспехе
TRY = 3
# Пауза между попытками
SLEEP_TIME = 1
#############################################################

################################### MS #################################
MS_TOKEN = "58155c07fd2d1daa5bad443581777572259bb80b"
MS_HEADERS = {
    "Content-Type": "application/json",
    "charset": "UTF-8",
    "Authorization": f"Bearer {MS_TOKEN}"
}
MS_DEFAULT_ORGANIZATION = '2261209a-715b-11e9-9107-504800016830'
MS_DEFAULT_STORE = 'ac4061a1-8020-11e3-cd9a-002590a28eca'
MS_DEFAULT_STATUS = '67e1468a-da3d-11e2-0645-7054d21a8d1e'
MS_CANCELED_STATUS = '67e1468a-da3d-11e2-0645-7054d21a8d1e'
MS_MINUS_STATUS = '73561d4a-c92f-11e3-afa0-002590a28eca'
MS_ORDER_STATUS_NOT_PAYED = '67e14cac-da3d-11e2-6e7c-7054d21a8d1e'
MS_DEFAULT_PRICE = '0f5aaccb-e802-4ddd-9c3b-6dabf7525226'
MS_FIELD_SOBRAN_BOOL = '6f0b062c-6bc8-11e8-9109-f8fc0010c3d6'
MS_FIELD_SOBRAN_INT = 'b9eb42fa-6bc8-11e8-9109-f8fc0010c981'
MS_LAST_DOCUMENTS = 20 # ms.get_last_orders_w_demand()
MS_DEMAND_STATUS_PAYED = 'b10a134d-af01-11e2-b55f-001b21d91495'
MS_DEMAND_STATUS_NOT_PAYED = '3a440969-a832-11e7-7a34-5acf00252a42'
########################################################################

################################# OZON #################################
OZON_TOKEN = "7660a38f-a39b-4a9a-99a4-32c5ffb44edf"
OZON_HEADERS = {
    "Client-Id": "118614",
    "Api-Key": OZON_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}
OZON_ORDERS_HOURS = 24
# OZON_TOKEN = "7c74f911-4371-4ba7-8bb0-59230ff02bc2"
# OZON_HEADERS = {
#     "Client-Id": "25318",
#     "Api-Key": OZON_TOKEN,
#     "Content-Type": "application/json",
#     "Accept": "application/json"
# }

OZON_DATA_FIELDS = [
    'delivering_date',
    'shipment_date'
]
OZON_COMMENT_FIELDS = {
    'STATUS': 'status',
    'ORDER_ID': 'order_id',
    'ORDER_NUMBER': 'order_number',
    'POSTING_NUMBER': 'posting_number',
    'DELIVERING_DATE': 'delivering_date',
    'SHIPMENT_DATE': 'shipment_date',

    'WAREHOUSE': 'delivery_method/warehouse',
    'WAREHOUSE_ID': 'delivery_method/warehouse_id',

    'REGION': 'analytics_data/region',
    'CITY': 'analytics_data/city',
    'DELIVERY_TYPE': 'analytics_data/delivery_type',
    'DELIVERY_DATE_END': 'analytics_data/delivery_date_end',

    'NAME': 'customer/name',
    'PHONE': 'customer/phone',
    'ADDRESS': 'customer/address/address_tail',
    'CUSTOMER_COMMENT': 'customer/address/comment',
    'EMAIL': 'customer/customer_email',

    'LABEL_UP_CODE': 'label_up_code',
    'LABEL_DOWN_CODE': 'label_down_code'
}
# OZON_SCHEMAS = ['fbo', 'fbs']
OZON_TYPES = ['fbs', 'realfbs', '']
OZON_ORDERS_OLD_DAYS = 10 # Period of orders to ckeck deliver db.get_last_orders()

OZON_HOURS_BEFOR_DELIVERED = 2

OZON_SLEEP_TIME = 20