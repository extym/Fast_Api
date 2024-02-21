import csv
import json

import requests

proxy = [
   {
      "name": "Название сделки",
      "price": 3422,
      "_embedded":{
         "contacts": [
            {
               "first_name":"Екатерина",
               "created_at":1608905348,
               "responsible_user_id":2004184,
               "updated_by":0,
               "custom_fields_values": [
                  {
                     "field_id":66186,
                     "values":[
                        {
                           "enum_id":193200,
                           "value":"example@example.com"
                        }
                     ]
                  },
                  {
                     "field_id":66192,
                     "values":[
                        {
                           "enum_id":193226,
                           "value":"+79123456789"
                        }
                     ]
                  }
               ]
            }
         ],
         "companies":[
            {
               "name":"ООО Рога и Копыта"
            }
         ]
      },
      "created_at":1608905348,
      "responsible_user_id":2004184,
      "custom_fields_values":[
         {
            "field_id":1286573,
            "values":[
               {
                  "value":"Поле текст"
               }
            ]
         },
         {
            "field_id":1286575,
            "values":[
               {
                  "enum_id":2957741
               },
               {
                  "enum_id":2957743
               }
            ]
         }
      ],
      "status_id":33929752,
      "pipeline_id":3383152,
      "request_id": "qweasd"
   },
   {
      "name": "Название сделки",
      "price": 3422,
      "_embedded":{
         "metadata":{
            "category": "forms",
            "form_id": 123,
            "form_name": "Форма на сайте",
            "form_page": "https://example.com",
            "form_sent_at": 1608905348,
            "ip": "8.8.8.8",
            "referer": "https://example.com/form.html"
         },
         "contacts":[
            {
               "first_name":"Евгений",
               "custom_fields_values":[
                  {
                     "field_code":"EMAIL",
                     "values":[
                        {
                           "enum_code":"WORK",
                           "value":"unsorted_example@example.com"
                        }
                     ]
                  },
                  {
                     "field_code":"PHONE",
                     "values":[
                        {
                           "enum_code":"WORK",
                           "value":"+79129876543"
                        }
                     ]
                  }
               ]
            }
         ]
      },
      "status_id":33929749,
      "pipeline_id":3383152,
      "request_id": "uns_qweasd"
   }
]


ll = {
    'id': 'u2i-tR8TD8ZL21cd_anNRU2U6g',
    'context':
	    {
            'type': 'item',
		    'value': {
                'id': 3364551629,
                'title': 'Mercedes-benz A2822020019 ролик обводной',
                'user_id': 353207078,
		        'images': {
			        'main': {
                        '140x105': 'https://30.img.avito.st/image/1/1.yzR1HbaxZ91bvLfebz7cf2G_Zd3HqGPf.M51vUWvhE19EdYffZn7u77T3xpQNuzVFGXqOO6QFufE'},
                        'count': 1
                },
                'status_id': 4,
                'price_string': '3\xa0873 ₽',
                'url': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/mercedes-benz_a2822020019_rolik_obvodnoy_3364551629',
                'location': {
                    'title': 'Санкт-Петербург', 'lat': 60.014356, 'lon': 30.452744
                }
            }
		},
    'created': 1693483353,
    'updated': 1693491453,
    'users':
        [
            {
                'id': 237130466,
                'name': 'Виктор Барановский',
                'parsing_allowed': True,
                'public_user_profile':  {
                    'user_id': 237130466,
                    'item_id': 3364551629,
                    'avatar': {
                        'default': 'https://51.img.avito.st/avatar/social/256x256/10243300051.jpg',
                        'images': {
                            '1024x1024': 'https://51.img.avito.st/avatar/social/1024x1024/10243300051.jpg',
                            '128x128': 'https://51.img.avito.st/avatar/social/128x128/10243300051.jpg',
                            '192x192': 'https://51.img.avito.st/avatar/social/192x192/10243300051.jpg',
                            '256x256': 'https://51.img.avito.st/avatar/social/256x256/10243300051.jpg',
                            '64x64': 'https://51.img.avito.st/avatar/social/64x64/10243300051.jpg',
                            '96x96': 'https://51.img.avito.st/avatar/social/96x96/10243300051.jpg'
                        }
                    },
                    'url': 'https://avito.ru/user/8e6fda67270371844cbd53e027b3d65f/profile?id=3364551629&iid=3364551629&src=messenger&page_from=from_item_messenger'
                }
            },
            {
                'id': 353207078,
                'name': 'JP Primer',
                'parsing_allowed': False,
                'public_user_profile': {
                    'user_id': 353207078,
                    'item_id': 3364551629,
                    'avatar': {
                        'default': 'https://83.img.avito.st/avatar/social/256x256/21206276983.jpg',
                        'images': {'1024x1024': 'https://83.img.avito.st/avatar/social/1024x1024/21206276983.jpg',
                                   '128x128': 'https://83.img.avito.st/avatar/social/128x128/21206276983.jpg',
                                   '192x192': 'https://83.img.avito.st/avatar/social/192x192/21206276983.jpg',
                                   '256x256': 'https://83.img.avito.st/avatar/social/256x256/21206276983.jpg',
                                   '64x64': 'https://83.img.avito.st/avatar/social/64x64/21206276983.jpg',
                                   '96x96': 'https://83.img.avito.st/avatar/social/96x96/21206276983.jpg'
                        }
                    },
                    'url': 'https://avito.ru/user/e08ab17ac60e1b42e74802141cb4f13b/profile?id=3364551629&iid=3364551629&src=messenger&page_from=from_item_messenger'
                }
            }
        ],
    'last_message': {
        'id': '30dcdf01286d817068dd457f980329f0',
        'author_id': 353207078,
        'created': 1693491453,
        'content': {
            'text': 'Пожалуйста!'
        },
        'type': 'text',
        'direction': 'out',
        'delivered': 1693491453
    }
}


chat_info_from_amo = {
  "event_type": "new_message",
  "payload": {
    "timestamp": 1639604903,
    "msec_timestamp": 1639604903161,
    "msgid": "my_int-5f2836a8ca476",
    "conversation_id": "my_int-d5a421f7f217",
    "sender": {
      "id": "my_int-manager1_user_id",
      "name": "Имя менеджера",
      "ref_id": "76fc2bea-902f-425c-9a3d-dcdac4766090"
    },
    "receiver": {
      "id": "my_int-1376265f-86df-4c49-a0c3-a4816df41af8",
      "avatar": "https://example.com/users/avatar.png",
      "name": "Вася клиент",
      "profile": {
        "phone": "+79151112233",
        "email": "example.client@example.com"
      },
      "profile_link": "https://example.com/profile/example.client"
    },
    "message": {
      "type": "text",
      "text": "Сообщение от менеджера 76fc2bea-902f-425c-9a3d-dcdac4766090"
    },
    "silent": True
  }
}


chat_info_from_avito = {
    "id":"u2i-TOYzRVLyb9Hw_l7u2aBTVg",
    "context":{
        "type":"item",
        "value":{
            "id":3364311913,
            "title":"TRW DF4110 Торм.диск пер.вент.280x24 4 отв",
            "user_id":353207078,
            "images":{
                "main":{
                    "140x105":"https://30.img.avito.st/image/1/1.UqbZzLax_k_3bS5M8cET7c1u_E9refpN.9gtAQBpllBaxOxqtFZcN1GwQgYgBGw2F_pIuGUXTeEU"
                },"count":1
            },
            "status_id":4,
            "price_string":"4 391 ₽",
            "url":"https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/trw_df4110_torm.disk_per.vent.280x24_4_otv_3364311913",
            "location":{
                "title":"Санкт-Петербург",
                "lat":60.014356,
                "lon":30.452744
            }
        }
    },
    "created":1693820808,
    "updated":1693842635,
    "users":[
        {
            "id":259749082,
            "name":"Александр  Иванович",
            "parsing_allowed":True,
            "public_user_profile":{
                "user_id":259749082,
                "item_id":3364311913,
                "avatar":{
                    "default":"https://20.img.avito.st/avatar/social/256x256/14986203020.jpg",
                    "images":{
                        "1024x1024":"https://20.img.avito.st/avatar/social/1024x1024/14986203020.jpg",
                        "128x128":"https://20.img.avito.st/avatar/social/128x128/14986203020.jpg",
                        "192x192":"https://20.img.avito.st/avatar/social/192x192/14986203020.jpg",
                        "256x256":"https://20.img.avito.st/avatar/social/256x256/14986203020.jpg",
                        "64x64":"https://20.img.avito.st/avatar/social/64x64/14986203020.jpg",
                        "96x96":"https://20.img.avito.st/avatar/social/96x96/14986203020.jpg"
                    }
                },
                "url":"https://avito.ru/user/76ee8581b9717b68e01cf5febe8b09ba/profile?id=3364311913\u0026iid=3364311913\u0026src=messenger\u0026page_from=from_item_messenger"
            }
        },
        {
            "id":353207078,
            "name":"JP Primer",
            "parsing_allowed":False,
            "public_user_profile":{
                "user_id":353207078,
                "item_id":3364311913,
                "avatar":{
                    "default":"https://04.img.avito.st/avatar/social/256x256/21889280304.jpg",
                    "images":{"1024x1024":"https://04.img.avito.st/avatar/social/1024x1024/21889280304.jpg",
                              "128x128":"https://04.img.avito.st/avatar/social/128x128/21889280304.jpg",
                              "192x192":"https://04.img.avito.st/avatar/social/192x192/21889280304.jpg",
                              "256x256":"https://04.img.avito.st/avatar/social/256x256/21889280304.jpg",
                              "64x64":"https://04.img.avito.st/avatar/social/64x64/21889280304.jpg",
                              "96x96":"https://04.img.avito.st/avatar/social/96x96/21889280304.jpg"
                              }
                },
                "url":"https://avito.ru/user/e08ab17ac60e1b42e74802141cb4f13b/profile?id=3364311913\u0026iid=3364311913\u0026src=messenger\u0026page_from=from_item_messenger"
            }
        }
    ],
    "last_message":{
        "id":"e737d71dcddc238d5a1db962f3fb6db9",
        "author_id":259749082,
        "created":1693842635,
        "content":{
            "text":"И какое время? Даётся на установку. Ну мало ли вдруг не подойдёт?"
        },
        "type":"text",
        "direction":"in",
        "delivered":1693842635
    }
}



webhook_avito_meddage = {
    'id': '97d14aac-97ac-40de-9220-4e6bdea78c5d',
    'version': 'v3.0.0',
    'timestamp': 1693842617,
    'payload': {
        'type': 'message',
        'user_id': {
            'id': '72ab5028eb846209e22f1c132e44a29e',
            'chat_id': 'u2i-TOYzRVLyb9Hw_l7u2aBTVg',
            'user_id': 353207078,
            'author_id': 259749082,
            'created': 1693842617,
            'type': 'text',
            'chat_type': 'u2i',
            'content': {
                'text': 'Покупку произвести у вас непосредственно там, на месте можно при осмотре.'
            },
            'item_id': 3364311913
        }
    }
}


webhook_amo_message = {
  "account_id": "52e591f7-c98f-4255-8495-827210138c81",
  "time": 1639572261,
  "message": {
    "receiver": {
      "id": "2ed64e26-70a1-4857-8382-bb066a076219",
      "phone": "79161234567",
      "email": "example.client@example.com",
      "client_id":"my_int-1376265f-86df-4c49-a0c3-a4816df41af8"
    },
    "sender": {
      "id": "76fc2bea-902f-425c-9a3d-dcdac4766090"
    },
    "conversation": {
      "id": "8e4d4baa-9e6c-4a88-838a-5f62be227bdc",
      "client_id":"my_int-d5a421f7f218"
    },
    "source":{
      "external_id":"78001234567"
    },
    "timestamp": 1639572260,
    "msec_timestamp": 1639572260980,
    "message": {
      "id": "0371a0ff-b78a-4c7b-8538-a7d547e10692",
      "type": "picture",
      "text": "Текст сообщения Сделка #15926745",
      "markup": {
        "mode": "inline",
        "buttons": [
          [
            {
              "text":"Принять заказ"
            },
            {
              "text":"Отменить заказ"
            }
          ]
        ]
      },
      "tag": "",
      "media": "https://amojo.amocrm.ru/attachments/image.jpg",
      "thumbnail": "https://amojo.amocrm.ru/attachments/image_320x200.jpg",
      "file_name": "",
      "file_size": 0,
      "template": {
        "id": 7103,
        "content": "Текст сообщения {{lead.name}}",
        "params": [
          {
            "key": "{{lead.id}}",
            "value": "15926745"
          }
        ]
      }
    }
  }
}

webhook_amo_message_v2 = {'account_id': 'd2914d60-a44a-4625-881b-d9e237592dce', 'time': 1696335541, 'message': {'receiver': {'id': 'f6d6cccf-660b-478c-b1ad-c7decb1fdae2', 'name': 'Андрей', 'client_id': '26665641'}, 'sender': {'id': '43d62858-70f2-4afc-8776-39892a08f690', 'name': ''}, 'conversation': {'id': '4b10d0e2-32ee-41b7-94e5-e490b007f97e', 'client_id': 'u2i-sjJYEdKG89VKhGV6SDQIEw'}, 'timestamp': 1696335541, 'msec_timestamp': 1696335541851, 'message': {'id': '16adb82f-1f8d-4a04-8fb3-7acbc0f8891a', 'type': 'text', 'text': 'whats up?', 'markup': None, 'tag': '', 'media': '', 'thumbnail': '', 'file_name': '', 'file_size': 0}}}

test_unread_message = {
    "id":"64bff4ff-94e2-45a1-85e4-7e3f464c4cf8",
    "version":"v3.0.0",
    "timestamp":1693831255,
    "payload":{
        "type":"message",
        "value":{
            "id":"da47387aa97e86b10fdd51394262a815",
            "chat_id":"u2i-xNG6BsZqGy6XaZaW0oZvlQ",
            "user_id":353207078,
            "author_id":121185841,
            "created":1693831255,
            "type":"text",
            "chat_type":"u2i",
            "content":{
                "text":"\xd0\xaf \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb8\xd0\xbb\xd0\xb0 \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 \xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd0\xbe"
            },
            "item_id":3363702577
        }
    }
}


test_new_message_to_amo = {
      "event_type": "new_message",
      "payload": {
            "timestamp": 1639660529,
            "msec_timestamp": 1639660529379,
            "msgid": "my_int-5f2836a8ca481",
            "conversation_id": "my_int-d5a421f7f218",
            "sender": {
                  "id": "my_int-1376265f-86df-4c49-a0c3-a4816df41af8",
                  "avatar": "https://images.pexels.com/photos/10050979/pexels-photo-10050979.jpeg?auto=compress&cs=tinysrgb&dpr=2&w=500",
                  "profile": {
                    "phone": "+79151112233",
                    "email": "example.client@example.com"
                  },
                  "profile_link": "https://example.com/profile/example.client",
                  "name": "Вася клиент"
            },
            "message": {
                  "type": "text",
                  "text": "Сообщение от клиента"
            },
            "silent": False
      }
}



parts_soft_hook = {
    "order":{
        "jsonb_fields":{
            "amo_crm_last_status_id":"59812618",
            "amo_crm_order_items_note_id":197190209
        },
        "order_options":{},
        "customer_id":224,
        "amo_crm_id":"27389745",
        "id":573,
        "delivery_type_id":None,
        "order_id":573,
        "payment_type_id":None,
        "comment":None,
        "created_at":"2023-09-08T12:47:33.232 03:00",
        "updated_at":"2023-09-08T12:47:34.146 03:00",
        "id_1c":"site-573-Valeriy (224)",
        "user_id":None,
        "send_to_supplier":None,
        "order_status_type_id":1,"name":None,
        "second_name":None,
        "family_name":None,
        "warehouse_id":None,
        "pay_status_id":None,
        "wait_assembling":False,
        "region_order_id":None,
        "initial_currency":None,
        "currency_rate":1.0,
        "is_archive":False,
        "check_vin":False,
        "paid":False,
        "auto_id":None,
        "source_type":"client",
        "service_booking":False,
        "sys_info":None,
        "answer_guid":"2fe97116-7034-2811-c1a4-0d3dee0adb15",
        "answer_at":None,
        "answer_ip":None,
        "price_id":None,
        "delivery_point_id":None,
        "roistat_visit":None,
        "lead_id":None,
        "price_supplier_order_option_id":None,
        "we_make_call":False,
        "we_make_call_at":None,
        "moysklad_id":None,
        "wait_sync":True,
        "order_uniq_key":"224-1",
        "customer_order_id":1,
        "external_crm_id":None,
        "disable_balance_recalc":False,
        "load_order_client_number":None,
        "client_file_name":None,
        "business_ru_id":None,
        "wait_update_balance":False,
        "close_lock_at":None,
        "load_customer_id":None,
        "close_lock_id":None,
        "region_id":1,
        "marketplace_data":{},
        "marketplace_id":None,
        "clear_marketplace_id":None,
        "we_sent_answer_at":None,
        "remote_web_service_id":None,
        "marketplace_confirm_fail_msg":None,
        "marketplace_confirm_send_at":None,
        "marketplace_confirm_count":0,
        "is_manual_reorder":False,
        "order_specification_id":None,
        "bill_needs_to_be_created":False,
        "order_items":
            [
                {
                    "id":688,
                    "customer_id":224,
                    "oem":"NSP052601000Q1F",
                    "make_name":"NSP",
                    "detail_name":"Фара правая NISSAN Terrano (14-) (10702070/010520/0088963 КИТАЙ)",
                    "cost":10248.0,
                    "first_cost":8759.0,
                    "qnt":1,
                    "status":{
                        "order_status_type":{
                            "id":1,
                            "name":"Обрабатывается",
                            "code":"processing",
                            "description":"",
                            "color":"56aaff",
                            "position":None,
                            "confirmation_body":"Вы можете вывести его в шаблоне {{order_item.status.confirmation_body}}",
                            "send_confirm":True,
                            "created_at":"2023-03-23T17:25:52.857 03:00",
                            "updated_at":"2023-07-10T18:16:40.819 03:00",
                            "font_color":"000000",
                            "default":False,
                            "id_1c":None,
                            "sms":"Вы заказывали {{order_item.detail_name}} {{order_item.oem}} {{order_item.make_name}}",
                            "send_sms":True,
                            "notify_overdue_reaction":False,
                            "notify_overdue_reaction_day":3,
                            "overdue_sms_template":"",
                            "send_overdue_sms":False,
                            "admin_notify_overdue_reaction":True,
                            "destroy_overdue_reaction":True,
                            "destroy_overdue_reaction_day":3,
                            "wait_group_overdue":False,
                            "destroy_status_comment":"",
                            "is_priority":False,
                            "send_to_outdated":False,
                            "is_set_on_accept_product_return":None,
                            "sms_discount_groups":[],
                            "disable_check_status":False,
                            "send_manager_notification":True,
                            "send_region_notification":False,
                            "send_sms_group_notification":True,
                            "send_sms_group_template":"Ваш заказ №{{order.order_id}} перешел в статус {{status.name}}",
                            "send_email_group_subject_template":"",
                            "send_email_group_template":"",
                            "send_email_group_notification":False,
                            "send_email_manager_group_notification":True,
                            "send_email_region_group_notification":False,
                            "zzap_status_id":"",
                            "zzap_status_description":"","zzap_group_status_id":"",
                            "zzap_group_status_description":"",
                            "max_hour_in_status":0.0,"max_hour_in_status_change_to_status_id":None,
                            "send_email_delivery_point_group_notification":False,"send_email_delivery_point_notification":False,
                            "order_group_send_to_archive":False,"order_item_send_to_archive":False,"excude_from_invoice_load":False,
                            "exclude_for_delivery_date_problem":False,"delete_unpaid_bill":False,
                            "gettzap_status_id":"","gettzap_status_description":"","gettzap_group_status_id":"",
                            "gettzap_group_status_description":"","additional_email":"","additional_group_email":"",
                            "jsonb_fields":{"user_sms":"Создан заказ {{order_item.detail_name}} {{order_item.oem}} {{order_item.make_name}}, статус заказа изменился на {{order_item.status.name}}, кол. заказано {{order_item.qnt}}, актуальное кол. {{order_item.current_qnt}}",
                                            "send_user_sms":"1",
                                            "send_order_user_sms":"1",
                                            "tg_send_contact_mode":"",
                                            "tg_send_bill_link_button":"1",
                                            "send_order_manager_notification":"1",
                                            "order_admin_notify_overdue_reaction":"0",
                                            "send_email_order_manager_group_notification":"1"
                                            },
                            "set_when_web_service_decline":False,
                            "exclude_from_bill_actual":False,
                            "email_discount_groups":[2,3],
                            "send_answere":False
                        }
                    },
                    "price_name":"MPARTS https://v01.ru/",
                    "created_at":"2023-09-08T12:47:33.224 03:00",
                    "updated_at":"2023-09-08T12:47:33.311 03:00",
                    "import_at":None,
                    "comment":"",
                    "order_number":None,
                    "delivery_date":None,
                    "status_id":1,
                    "order_id":573,
                    "raw_price":8759.0,
                    "price_id":15,
                    #"sys_info":"{\\"central_warehouse\\":False,\\"client_visible_cost\\":10248,\\"client_visible_cost_currency\\":\\"RUB\\",\\"cross_sources\\":[],\\"detail_comment\\":\\"\\",\\"goods_img_url\\":\\"https://img-server-10.parts-soft.ru/images/1554/14384427\\",\\"hide_visible_sup_logo_www\\":True,\\"is_outdated_oem\\":False,\\"item_key\\":\\"nsp052601000q1f\\",\\"max_delivery_in_hour\\":24,\\"min_delivery_in_hour\\":24,\\"price_request_guid_id\\":\\"2e1fdb71-a6d6-4aa2-bde1-b0222a5f5c52\\",\\"pricing_log\\":None,\\"raw_make_name\\":\\"NSP\\",\\"requested_make_name\\":\\"NSP\\",\\"requested_oem\\":\\"NSP052601000Q1F\\",\\"return_without_problem\\":True,\\"return_without_problem_comment\\":\\"Возврат без удержания\\",\\"search_comment\\":\\"\\",\\"source_oem\\":\\"NSP052601000Q1F\\",\\"source_rate\\":1,\\"stat_group\\":\\"0\\",\\"stat_group_type\\":\\"bad\\",\\"sup_logo\\":\\"12909\\",\\"sync_supplier_info\\":False,\\"visible_delivery_day\\":\\"1 день \\",\\"visible_sup_logo\\":\\"\\",\\"visible_sup_logo_www\\":\\"MP\\",\\"volume\\":\\"\\",\\"weight\\":3.3,\\"weightMethod\\":\\"api\\",\\"ws_raw_cost\\":8759.0,\\"ws_supplier_code\\":12909,\\"checkout_options\\":\\"None\\",\\"min_qnt\\":1}",
                    "supplier_order_item_id":None,
                    "qnt_accept":None,
                    "qnt_income":None,
                    "id_1c":"C224O573I688",
                    "min_delivery_day":1,
                    "max_delivery_day":1,
                    "add_in_ws":False,
                    "gtd":None,
                    "country":None,
                    "company_comment":None,
                    "delivery_comment":None,
                    "last_status_change_at":"2023-09-08T12:47:33.225 03:00",
                    "visible_order_id":573,"customer_region_id":1,
                    "user_name":"Сергей",
                    "status_code":"processing",
                    "customer_phone":" 7 (931) 252-81-57",
                    "customer_title":"Валерий (224)",
                    "customer_region_name":"Санкт-Петербург",
                    "price_region_name":"Санкт-Петербург",
                    "price_region_id":1,
                    "last_status_notify":None,
                    "is_region_pair":False,
                    "region_order_item_id":None,
                    "order_complete_at":None,
                    "real_delivery_day":None,
                    "dialogs_count":0,
                    "is_archive":False,
                    "external_order_id":None,
                    "external_order_type":None,
                    "ts_order_item_info":"\' 7\':151 \'-57\':155 \'-81\':154 \'/images/1554/14384427\':34 \'0\':104 \'1\':101,119,147 \'10248\':19 \'10702070/010520/0088963\':8 \'12909\':111,141 \'14\':7 \'15\':12 \'224\':156 \'24\':52,57 \'252\':153 \'2e1\':62 \'3.3\':131 \'4aa2\':66 \'573\':149 \'8759.0\':137 \'931\':152 \'a6d6\':65 \'api\':133 \'b0222a5f5c52\':68 \'bad\':108 \'bde1\':67 \'c224o573i688\':148 \'central\':13 \'checkout\':142 \'client\':16,20 \'code\':140 \'comment\':28,90,95 \'cost\':18,22,136 \'cross\':25 \'currenc\':23 \'day\':118 \'deliveri\':49,54,117 \'detail\':27 \'fals\':15,44,115 \'fdb71\':64 \'fdb71-a6d6-4aa2-bde1-b0222a5f5c52\':63 \'good\':29 \'group\':103,106 \'guid\':60 \'hide\':35 \'hour\':51,56 \'id\':61 \'img\':30 \'img-server-10.parts-soft.ru\':33 \'img-server-10.parts-soft.ru/images/1554/14384427\':32 \'info\':114 \'item\':45 \'key\':46 \'log\':70 \'logo\':38,110,123,126 \'make\':73,77 \'max\':48 \'min\':53,145 \'mp\':128 \'mpart\':10 \'name\':74,78 \'nissan\':5 \'None\':144 \'nsp\':2,75,79 \'nsp052601000q1f\':1,47,82,98 \'None\':71 \'oem\':43,81,97 \'option\':143 \'outdat\':42 \'price\':58,69 \'problem\':85,89 \'qnt\':146 \'rate\':100 \'raw\':72,135 \'request\':59,76,80 \'return\':83,87 \'rub\'"
                }
            ]
        }
    }


tt = {'event_type': 'new_message', 'payload': {'timestamp': 1694188853, 'msec_timestamp': 1694188853169, 'msgid': 'ca84673cd3fe5b43c00e0cdae08547ab', 'conversation_id': 'u2i-NYGSUv0QQ_0ZiJL~94eBJA', 'sender': {'id': 59108686, 'avatar': 'https://static.avito.ru/stub_avatars/_/14_256x256.png', 'profile': {'phone': '', 'email': ''}, 'profile_link': 'https://avito.ru/user/97e2f94f0813176d08944ebd85cda862/profile?id=3364589989&iid=3364589989&src=messenger&page_from=from_item_messenger', 'name': 'Николай'}, 'message': {'type': 'text', 'text': 'Добрый вечер\nРейка в наличии?'}, 'silent': False}}

test = {
    '_page': 1,
    '_links': {
        'self': {
            'href': 'https://amo3431ru.amocrm.ru/api/v4/leads?page=1&limit=20&order=created_at'
        },
        'next': {
            'href': 'https://amo3431ru.amocrm.ru/api/v4/leads?page=2&limit=20&order=created_at'
        }
    },
    '_embedded': {
        'leads': [
            {
                'id': 25813923,
                'name': 'Новая сделка с [Входящий звонок +79052738093]',
                'price': 0,
                'responsible_user_id': 9983934,
                'group_id': 0,
                'status_id': 143,
                'pipeline_id': 7155526,
                'loss_reason_id': 15601354,
                'created_by': 9983930,
                'updated_by': 9983930,
                'created_at': 1692861891,
                'updated_at': 1692888780,
                'closed_at': 1692888780,
                'closest_task_at': None,
                'is_deleted': False,
                'custom_fields_values': None,
                'score': None,
                'account_id': 31247590,
                'labor_cost': None,
                '_links': {
                    'self': {
                        'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25813923?page=1&limit=20&order=created_at'
                    }
                },
                '_embedded': {
                'tags': [],
                'companies': []
                }
            },
            {
                'id': 25771571,
                'name': 'Новая сделка с [Входящий звонок +79818149999]',
                'price': 0,
                'responsible_user_id': 9983934,
                'group_id': 0,
                'status_id': 143,
                'pipeline_id': 7155526,
                'loss_reason_id': None,
                'created_by': 9983930, 'updated_by': 9983930, 'created_at': 1692803915, 'updated_at': 1692891150,
                'closed_at': 1692891150, 'closest_task_at': None, 'is_deleted': False,
                'custom_fields_values': None, 'score': None, 'account_id': 31247590,
                'labor_cost': None,
                '_links': {
                    'self': {
                        'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25771571?page=1&limit=20&order=created_at'
                    }
                },
                '_embedded': {
                    'tags': [],
                    'companies': []
                }
            },
            {
                'id': 25767727,
                'name': 'Новая сделка с [Входящий звонок +79527917552]',
                'price': 0, 'responsible_user_id': 9983934,
                'group_id': 0, 'status_id': 143,
                'pipeline_id': 7155526, 'loss_reason_id': None,
                'created_by': 9983930, 'updated_by': 9983930, 'created_at': 1692800023,
                'updated_at': 1692957093, 'closed_at': 1692957093, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': None, 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25767727?page=1&limit=20&order=created_at'}},
                '_embedded': {'tags': [], 'companies': []}}, {'id': 25732023, 'name': 'Motorad 709-80/95K Термостат', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692797389, 'updated_at': 1692957242, 'closed_at': 1692957242, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Motorad 709-80/95K Термостат'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/motorad_709-8095k_termostat_3436678282'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25732023?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25697061, 'name': 'Mobiland 603100221 шрус наружный передний для а/м', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692794253, 'updated_at': 1692957260, 'closed_at': 1692957260, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Mobiland 603100221 шрус наружный передний для а/м'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/mobiland_603100221_shrus_naruzhnyy_peredniy_dlya_am_3436591350'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25697061?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25478969, 'name': 'Ford 1447508 Подножка сдвижной двери. Transit TT9', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692618064, 'updated_at': 1692973433, 'closed_at': 1692973433, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Ford 1447508 Подножка сдвижной двери. Transit TT9'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/ford_1447508_podnozhka_sdvizhnoy_dveri._transit_tt9_3403943407'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25478969?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25761021, 'name': 'Zimmermann 290.2264.52 Торм.диск пер.вент.355x32 5', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692797978, 'updated_at': 1693235863, 'closed_at': 1693235863, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Zimmermann 290.2264.52 Торм.диск пер.вент.355x32 5'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/zimmermann_290.2264.52_torm.disk_per.vent.355x32_5_3435853015'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25761021?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25735957, 'name': 'Luzar lric 0801 Интеркулер', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692797478, 'updated_at': 1693235943, 'closed_at': 1693235943, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Luzar lric 0801 Интеркулер'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/luzar_lric_0801_interkuler_3435816856'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25735957?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25650247, 'name': 'Miles BLC0016 Высоковольтные провода зажигания for', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692728554, 'updated_at': 1693235961, 'closed_at': 1693235961, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Miles BLC0016 Высоковольтные провода зажигания for'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/miles_blc0016_vysokovoltnye_provoda_zazhiganiya_for_3436472985'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25650247?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25650847, 'name': 'Miles GA10048 шрус toyota avensis T220/T250/coroll', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692731228, 'updated_at': 1693235988, 'closed_at': 1693235988, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Miles GA10048 шрус toyota avensis T220/T250/coroll'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/miles_ga10048_shrus_toyota_avensis_t220t250coroll_3436658919'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25650847?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25574249, 'name': 'Gates TH35991 Термостат охлаждающей жидкости', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692715257, 'updated_at': 1693236018, 'closed_at': 1693236018, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Gates TH35991 Термостат охлаждающей жидкости'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/gates_th35991_termostat_ohlazhdayuschey_zhidkosti_3436062523'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25574249?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25573403, 'name': 'Airline aprd04 Манометр цифровой ЖК дисплей 7 атм', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692713464, 'updated_at': 1693236166, 'closed_at': 1693236166, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Airline aprd04 Манометр цифровой ЖК дисплей 7 атм'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/airline_aprd04_manometr_tsifrovoy_zhk_displey_7_atm_3403708811'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25573403?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25567837, 'name': 'BMW 17137639023 Пробка радиатора', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692709715, 'updated_at': 1693236184, 'closed_at': 1693236184, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'BMW 17137639023 Пробка радиатора'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/bmw_17137639023_probka_radiatora_3404627392'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25567837?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25562093, 'name': 'Chrysler 68188865AA клапан вентиляции картера', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692704921, 'updated_at': 1693236197, 'closed_at': 1693236197, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Chrysler 68188865AA клапан вентиляции картера'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/chrysler_68188865aa_klapan_ventilyatsii_kartera_3403834953'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25562093?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25545157, 'name': 'KYB 341851 Амортизатор подвески задний', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692695462, 'updated_at': 1693236282, 'closed_at': 1693236282, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'KYB 341851 Амортизатор подвески задний'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/kyb_341851_amortizator_podveski_zadniy_3436109485'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25545157?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25541891, 'name': 'General motors 93160377 антифриз', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692690902, 'updated_at': 1693236325, 'closed_at': 1693236325, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'General motors 93160377 антифриз'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/general_motors_93160377_antifriz_3436667992'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25541891?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25510385, 'name': 'Fenox CTC3504 Суппорт Mitsubishi Lancer viii (CX,C', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692647363, 'updated_at': 1693236401, 'closed_at': 1693236401, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Fenox CTC3504 Суппорт Mitsubishi Lancer viii (CX,C'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/fenox_ctc3504_support_mitsubishi_lancer_viii_cxc_3403742739'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25510385?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25655535, 'name': 'VAG 5K0698451E Колодки тормозные дисковые', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983934, 'created_at': 1692768333, 'updated_at': 1693307107, 'closed_at': 1693307107, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'VAG 5K0698451E Колодки тормозные дисковые'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/vag_5k0698451e_kolodki_tormoznye_diskovye_3435728746'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25655535?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25693609, 'name': 'Teknorot B10182 Рычаг подвески BMW 5 серия G30, F9', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983934, 'created_at': 1692789524, 'updated_at': 1693317506, 'closed_at': 1693317506, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Teknorot B10182 Рычаг подвески BMW 5 серия G30, F9'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/teknorot_b10182_rychag_podveski_bmw_5_seriya_g30_f9_3435875736'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25693609?page=1&limit=20&order=created_at'}}, '_embedded': {'tags': [], 'companies': []}}, {'id': 25955555, 'name': 'Polmostrow 1003AL P10.03AL глушитель средняя часть', 'price': 0, 'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0, 'updated_by': 0, 'created_at': 1692987860, 'updated_at': 1693331350, 'closed_at': 1693306038, 'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [{'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text', 'values': [{'value': 'Polmostrow 1003AL P10.03AL глушитель средняя часть'}]}, {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url', 'values': [{'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/polmostrow_1003al_p10.03al_glushitel_srednyaya_chast_3435821014'}]}], 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25955555?page=1&limit=20&order=created_at'}},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                '_embedded': {'tags': [], 'companies': []}}]}}



ss = {"account_id":"af9945ff-1490-4cad-807d-945c15d88bec","title":"ScopeTitle","hook_api_version":"v2"}


current_amo_lead = {
    'id': 48936949,
    'name': 'Шланг системы охлаждения Land Rover Range Rover',
    'price': 990,
    'responsible_user_id': 10131478,
    'group_id': 0,
    'status_id': 142,
    'pipeline_id': 5420530,
    'loss_reason_id': None,
    'created_by': 0,
    'updated_by': 10131478,
    'created_at': 1707853146,
    'updated_at': 1707947243,
    'closed_at': 1707947243,
    'closest_task_at': None,
    'is_deleted': False,
    'custom_fields_values': [
        {
            'field_id': 1335423,
            'field_name': 'URL объявления',
            'field_code': None,
            'field_type': 'url',
            'values': [
                {
                    'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/shlang_sistemy_ohlazhdeniya_land_rover_range_rover_2984653549'}
            ]
        },
        {
            'field_id': 1335421,
            'field_name': 'Объявление',
            'field_code': None,
            'field_type': 'text',
            'values': [{
                'value': 'Шланг системы охлаждения Land Rover Range Rover'
                }
            ]
        },
        {
            'field_id': 1277245,
            'field_name': 'ID Заказа',
            'field_code': 'AMGBP_MOYSKLAD_ORDER_ID',
            'field_type': 'text',
            'values': [{'value': '12587'}]}],
    'score': None,
    'account_id': 30176098,
    'labor_cost': None,
    '_links': {
        'self': {
            'href': 'https://zakazjpexpressru.amocrm.ru/api/v4/leads/48936949?page=1&limit=250'
        }
    },
    '_embedded': {'tags': [{'id': 658679, 'name': 'JPexpress', 'color': None}], 'companies': []}}




import re

# validate_phone_number_pattern = "^\\+?[1-9][0-9]{7,14}$"
# res = re.match(validate_phone_number_pattern, "+12223334444") # Returns Match object
# print(res)
# # Extract phone number from a string
# extract_phone_number_pattern = "\\+?[1-9][0-9]{7,14}"
# data = re.findall(extract_phone_number_pattern, 'Здравствуйте, цена указана за ремень и ролик фирмы Гейтс. На 11182 ДВС подойдёт')
#
# print(data)

def read_fuck_log(fuck_log):
    proxy = []
    with open(fuck_log, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            pre = row[0].split('>')[1].split('<')
            proxy.append(int(pre[0]))
        print(proxy)


# read_fuck_log('./fuck-log-1.csv')


import pandas as pd
def read_sales(sales, price):
    proxy, faxy, maxy = [], {}, []

    data = pd.read_excel(sales)
    df = pd.DataFrame(data).values
    for row in df:
        faxy[row[0]] = row[:6]

    datas = pd.read_excel(price)
    ddf = pd.DataFrame(datas).values
    for ro in ddf:
        if ro[0] in faxy.keys():
            count = ro[6] - faxy.get(ro[0])[5]
            rero = list(ro[:6])
            if count > 0:
                rero.insert(6, int(count))
                proxy.append(rero)
                print(111, count, rero)
            else:

                continue
        elif ro[6] > 0:
            proxy.append(ro.copy()[:7])

    print('result', len(proxy))
    with open("proxy_price.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(proxy)
    # print(*proxy, sep='\n')


# read_sales('order_items_all.xls', 'price_rew.xls')

#
# extract_phone_number_pattern = "\\+?[7-9][0-9]{9,11}"
# stringg = 'Семь 9172213870' # 'Алпацкий Денис Юрьевич. Город Хабаровск,ул. Сысоева, дом 2, КВ. 20. 8 962 500 94 98. Отправить почтой РФ первым классом.'
# strrr = stringg.replace(' ', '')
# print(re.findall(extract_phone_number_pattern, strrr))
#
# print(strrr)

