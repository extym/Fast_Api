api_key_ozon_prod = '2e04404c-c6f9-4b35-b5c1-2af4ca56ce96'
api_key_ozon_admin = 'f519fdb3-98cb-4d11-9cd0-0c7cbd8c7b84'
host = 'https://api-seller.ozon.ru'
client_id = '90963'


last_id = 'WzQ2MzcyNzEyNyw0NjM3MjcxMjdd'

headers = {
        'Client-Id': client_id,
        'Api-Key': api_key_ozon_admin,
        'Content-Type': 'application/json'
    }


metod_get_list_products = '/v2/product/list'