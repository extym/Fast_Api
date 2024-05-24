import csv
import json
import os

import requests

proxy = [
    {
        "name": "Название сделки",
        "price": 3422,
        "_embedded": {
            "contacts": [
                {
                    "first_name": "Екатерина",
                    "created_at": 1608905348,
                    "responsible_user_id": 2004184,
                    "updated_by": 0,
                    "custom_fields_values": [
                        {
                            "field_id": 66186,
                            "values": [
                                {
                                    "enum_id": 193200,
                                    "value": "example@example.com"
                                }
                            ]
                        },
                        {
                            "field_id": 66192,
                            "values": [
                                {
                                    "enum_id": 193226,
                                    "value": "+79123456789"
                                }
                            ]
                        }
                    ]
                }
            ],
            "companies": [
                {
                    "name": "ООО Рога и Копыта"
                }
            ]
        },
        "created_at": 1608905348,
        "responsible_user_id": 2004184,
        "custom_fields_values": [
            {
                "field_id": 1286573,
                "values": [
                    {
                        "value": "Поле текст"
                    }
                ]
            },
            {
                "field_id": 1286575,
                "values": [
                    {
                        "enum_id": 2957741
                    },
                    {
                        "enum_id": 2957743
                    }
                ]
            }
        ],
        "status_id": 33929752,
        "pipeline_id": 3383152,
        "request_id": "qweasd"
    },
    {
        "name": "Название сделки",
        "price": 3422,
        "_embedded": {
            "metadata": {
                "category": "forms",
                "form_id": 123,
                "form_name": "Форма на сайте",
                "form_page": "https://example.com",
                "form_sent_at": 1608905348,
                "ip": "8.8.8.8",
                "referer": "https://example.com/form.html"
            },
            "contacts": [
                {
                    "first_name": "Евгений",
                    "custom_fields_values": [
                        {
                            "field_code": "EMAIL",
                            "values": [
                                {
                                    "enum_code": "WORK",
                                    "value": "unsorted_example@example.com"
                                }
                            ]
                        },
                        {
                            "field_code": "PHONE",
                            "values": [
                                {
                                    "enum_code": "WORK",
                                    "value": "+79129876543"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        "status_id": 33929749,
        "pipeline_id": 3383152,
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
                'public_user_profile': {
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
    "id": "u2i-TOYzRVLyb9Hw_l7u2aBTVg",
    "context": {
        "type": "item",
        "value": {
            "id": 3364311913,
            "title": "TRW DF4110 Торм.диск пер.вент.280x24 4 отв",
            "user_id": 353207078,
            "images": {
                "main": {
                    "140x105": "https://30.img.avito.st/image/1/1.UqbZzLax_k_3bS5M8cET7c1u_E9refpN.9gtAQBpllBaxOxqtFZcN1GwQgYgBGw2F_pIuGUXTeEU"
                }, "count": 1
            },
            "status_id": 4,
            "price_string": "4 391 ₽",
            "url": "https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/trw_df4110_torm.disk_per.vent.280x24_4_otv_3364311913",
            "location": {
                "title": "Санкт-Петербург",
                "lat": 60.014356,
                "lon": 30.452744
            }
        }
    },
    "created": 1693820808,
    "updated": 1693842635,
    "users": [
        {
            "id": 259749082,
            "name": "Александр  Иванович",
            "parsing_allowed": True,
            "public_user_profile": {
                "user_id": 259749082,
                "item_id": 3364311913,
                "avatar": {
                    "default": "https://20.img.avito.st/avatar/social/256x256/14986203020.jpg",
                    "images": {
                        "1024x1024": "https://20.img.avito.st/avatar/social/1024x1024/14986203020.jpg",
                        "128x128": "https://20.img.avito.st/avatar/social/128x128/14986203020.jpg",
                        "192x192": "https://20.img.avito.st/avatar/social/192x192/14986203020.jpg",
                        "256x256": "https://20.img.avito.st/avatar/social/256x256/14986203020.jpg",
                        "64x64": "https://20.img.avito.st/avatar/social/64x64/14986203020.jpg",
                        "96x96": "https://20.img.avito.st/avatar/social/96x96/14986203020.jpg"
                    }
                },
                "url": "https://avito.ru/user/76ee8581b9717b68e01cf5febe8b09ba/profile?id=3364311913\u0026iid=3364311913\u0026src=messenger\u0026page_from=from_item_messenger"
            }
        },
        {
            "id": 353207078,
            "name": "JP Primer",
            "parsing_allowed": False,
            "public_user_profile": {
                "user_id": 353207078,
                "item_id": 3364311913,
                "avatar": {
                    "default": "https://04.img.avito.st/avatar/social/256x256/21889280304.jpg",
                    "images": {"1024x1024": "https://04.img.avito.st/avatar/social/1024x1024/21889280304.jpg",
                               "128x128": "https://04.img.avito.st/avatar/social/128x128/21889280304.jpg",
                               "192x192": "https://04.img.avito.st/avatar/social/192x192/21889280304.jpg",
                               "256x256": "https://04.img.avito.st/avatar/social/256x256/21889280304.jpg",
                               "64x64": "https://04.img.avito.st/avatar/social/64x64/21889280304.jpg",
                               "96x96": "https://04.img.avito.st/avatar/social/96x96/21889280304.jpg"
                               }
                },
                "url": "https://avito.ru/user/e08ab17ac60e1b42e74802141cb4f13b/profile?id=3364311913\u0026iid=3364311913\u0026src=messenger\u0026page_from=from_item_messenger"
            }
        }
    ],
    "last_message": {
        "id": "e737d71dcddc238d5a1db962f3fb6db9",
        "author_id": 259749082,
        "created": 1693842635,
        "content": {
            "text": "И какое время? Даётся на установку. Ну мало ли вдруг не подойдёт?"
        },
        "type": "text",
        "direction": "in",
        "delivered": 1693842635
    }
}

proxy = ("u2i-TOYzRVLyb9Hw_l7u2aBTVg", '4391',
         "https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/trw_df4110_torm.disk_per.vent.280x24_4_otv_3364311913",
         'e737d71dcddc238d5a1db962f3fb6db9', 353207078, "TRW DF4110 Торм.диск пер.вент.280x24 4 отв",
         True, False, 0, 0)

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
            "client_id": "my_int-1376265f-86df-4c49-a0c3-a4816df41af8"
        },
        "sender": {
            "id": "76fc2bea-902f-425c-9a3d-dcdac4766090"
        },
        "conversation": {
            "id": "8e4d4baa-9e6c-4a88-838a-5f62be227bdc",
            "client_id": "my_int-d5a421f7f218"
        },
        "source": {
            "external_id": "78001234567"
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
                            "text": "Принять заказ"
                        },
                        {
                            "text": "Отменить заказ"
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

webhook_amo_message_v2 = {'account_id': 'd2914d60-a44a-4625-881b-d9e237592dce', 'time': 1696335541, 'message': {
    'receiver': {'id': 'f6d6cccf-660b-478c-b1ad-c7decb1fdae2', 'name': 'Андрей', 'client_id': '26665641'},
    'sender': {'id': '43d62858-70f2-4afc-8776-39892a08f690', 'name': ''},
    'conversation': {'id': '4b10d0e2-32ee-41b7-94e5-e490b007f97e', 'client_id': 'u2i-sjJYEdKG89VKhGV6SDQIEw'},
    'timestamp': 1696335541, 'msec_timestamp': 1696335541851,
    'message': {'id': '16adb82f-1f8d-4a04-8fb3-7acbc0f8891a', 'type': 'text', 'text': 'whats up?', 'markup': None,
                'tag': '', 'media': '', 'thumbnail': '', 'file_name': '', 'file_size': 0}}}

test_unread_message = {
    "id": "64bff4ff-94e2-45a1-85e4-7e3f464c4cf8",
    "version": "v3.0.0",
    "timestamp": 1693831255,
    "payload": {
        "type": "message",
        "value": {
            "id": "da47387aa97e86b10fdd51394262a815",
            "chat_id": "u2i-xNG6BsZqGy6XaZaW0oZvlQ",
            "user_id": 353207078,
            "author_id": 121185841,
            "created": 1693831255,
            "type": "text",
            "chat_type": "u2i",
            "content": {
                "text": "\xd0\xaf \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb8\xd0\xbb\xd0\xb0 \xd1\x87\xd0\xb5\xd1\x80\xd0\xb5\xd0\xb7 \xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd0\xbe"
            },
            "item_id": 3363702577
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
    "order": {
        "jsonb_fields": {
            "amo_crm_last_status_id": "59812618",
            "amo_crm_order_items_note_id": 197190209
        },
        "order_options": {},
        "customer_id": 224,
        "amo_crm_id": "27389745",
        "id": 573,
        "delivery_type_id": None,
        "order_id": 573,
        "payment_type_id": None,
        "comment": None,
        "created_at": "2023-09-08T12:47:33.232 03:00",
        "updated_at": "2023-09-08T12:47:34.146 03:00",
        "id_1c": "site-573-Valeriy (224)",
        "user_id": None,
        "send_to_supplier": None,
        "order_status_type_id": 1, "name": None,
        "second_name": None,
        "family_name": None,
        "warehouse_id": None,
        "pay_status_id": None,
        "wait_assembling": False,
        "region_order_id": None,
        "initial_currency": None,
        "currency_rate": 1.0,
        "is_archive": False,
        "check_vin": False,
        "paid": False,
        "auto_id": None,
        "source_type": "client",
        "service_booking": False,
        "sys_info": None,
        "answer_guid": "2fe97116-7034-2811-c1a4-0d3dee0adb15",
        "answer_at": None,
        "answer_ip": None,
        "price_id": None,
        "delivery_point_id": None,
        "roistat_visit": None,
        "lead_id": None,
        "price_supplier_order_option_id": None,
        "we_make_call": False,
        "we_make_call_at": None,
        "moysklad_id": None,
        "wait_sync": True,
        "order_uniq_key": "224-1",
        "customer_order_id": 1,
        "external_crm_id": None,
        "disable_balance_recalc": False,
        "load_order_client_number": None,
        "client_file_name": None,
        "business_ru_id": None,
        "wait_update_balance": False,
        "close_lock_at": None,
        "load_customer_id": None,
        "close_lock_id": None,
        "region_id": 1,
        "marketplace_data": {},
        "marketplace_id": None,
        "clear_marketplace_id": None,
        "we_sent_answer_at": None,
        "remote_web_service_id": None,
        "marketplace_confirm_fail_msg": None,
        "marketplace_confirm_send_at": None,
        "marketplace_confirm_count": 0,
        "is_manual_reorder": False,
        "order_specification_id": None,
        "bill_needs_to_be_created": False,
        "order_items":
            [
                {
                    "id": 688,
                    "customer_id": 224,
                    "oem": "NSP052601000Q1F",
                    "make_name": "NSP",
                    "detail_name": "Фара правая NISSAN Terrano (14-) (10702070/010520/0088963 КИТАЙ)",
                    "cost": 10248.0,
                    "first_cost": 8759.0,
                    "qnt": 1,
                    "status": {
                        "order_status_type": {
                            "id": 1,
                            "name": "Обрабатывается",
                            "code": "processing",
                            "description": "",
                            "color": "56aaff",
                            "position": None,
                            "confirmation_body": "Вы можете вывести его в шаблоне {{order_item.status.confirmation_body}}",
                            "send_confirm": True,
                            "created_at": "2023-03-23T17:25:52.857 03:00",
                            "updated_at": "2023-07-10T18:16:40.819 03:00",
                            "font_color": "000000",
                            "default": False,
                            "id_1c": None,
                            "sms": "Вы заказывали {{order_item.detail_name}} {{order_item.oem}} {{order_item.make_name}}",
                            "send_sms": True,
                            "notify_overdue_reaction": False,
                            "notify_overdue_reaction_day": 3,
                            "overdue_sms_template": "",
                            "send_overdue_sms": False,
                            "admin_notify_overdue_reaction": True,
                            "destroy_overdue_reaction": True,
                            "destroy_overdue_reaction_day": 3,
                            "wait_group_overdue": False,
                            "destroy_status_comment": "",
                            "is_priority": False,
                            "send_to_outdated": False,
                            "is_set_on_accept_product_return": None,
                            "sms_discount_groups": [],
                            "disable_check_status": False,
                            "send_manager_notification": True,
                            "send_region_notification": False,
                            "send_sms_group_notification": True,
                            "send_sms_group_template": "Ваш заказ №{{order.order_id}} перешел в статус {{status.name}}",
                            "send_email_group_subject_template": "",
                            "send_email_group_template": "",
                            "send_email_group_notification": False,
                            "send_email_manager_group_notification": True,
                            "send_email_region_group_notification": False,
                            "zzap_status_id": "",
                            "zzap_status_description": "", "zzap_group_status_id": "",
                            "zzap_group_status_description": "",
                            "max_hour_in_status": 0.0, "max_hour_in_status_change_to_status_id": None,
                            "send_email_delivery_point_group_notification": False,
                            "send_email_delivery_point_notification": False,
                            "order_group_send_to_archive": False, "order_item_send_to_archive": False,
                            "excude_from_invoice_load": False,
                            "exclude_for_delivery_date_problem": False, "delete_unpaid_bill": False,
                            "gettzap_status_id": "", "gettzap_status_description": "", "gettzap_group_status_id": "",
                            "gettzap_group_status_description": "", "additional_email": "",
                            "additional_group_email": "",
                            "jsonb_fields": {
                                "user_sms": "Создан заказ {{order_item.detail_name}} {{order_item.oem}} {{order_item.make_name}}, статус заказа изменился на {{order_item.status.name}}, кол. заказано {{order_item.qnt}}, актуальное кол. {{order_item.current_qnt}}",
                                "send_user_sms": "1",
                                "send_order_user_sms": "1",
                                "tg_send_contact_mode": "",
                                "tg_send_bill_link_button": "1",
                                "send_order_manager_notification": "1",
                                "order_admin_notify_overdue_reaction": "0",
                                "send_email_order_manager_group_notification": "1"
                            },
                            "set_when_web_service_decline": False,
                            "exclude_from_bill_actual": False,
                            "email_discount_groups": [2, 3],
                            "send_answere": False
                        }
                    },
                    "price_name": "MPARTS https://v01.ru/",
                    "created_at": "2023-09-08T12:47:33.224 03:00",
                    "updated_at": "2023-09-08T12:47:33.311 03:00",
                    "import_at": None,
                    "comment": "",
                    "order_number": None,
                    "delivery_date": None,
                    "status_id": 1,
                    "order_id": 573,
                    "raw_price": 8759.0,
                    "price_id": 15,
                    # "sys_info":"{\\"central_warehouse\\":False,\\"client_visible_cost\\":10248,\\"client_visible_cost_currency\\":\\"RUB\\",\\"cross_sources\\":[],\\"detail_comment\\":\\"\\",\\"goods_img_url\\":\\"https://img-server-10.parts-soft.ru/images/1554/14384427\\",\\"hide_visible_sup_logo_www\\":True,\\"is_outdated_oem\\":False,\\"item_key\\":\\"nsp052601000q1f\\",\\"max_delivery_in_hour\\":24,\\"min_delivery_in_hour\\":24,\\"price_request_guid_id\\":\\"2e1fdb71-a6d6-4aa2-bde1-b0222a5f5c52\\",\\"pricing_log\\":None,\\"raw_make_name\\":\\"NSP\\",\\"requested_make_name\\":\\"NSP\\",\\"requested_oem\\":\\"NSP052601000Q1F\\",\\"return_without_problem\\":True,\\"return_without_problem_comment\\":\\"Возврат без удержания\\",\\"search_comment\\":\\"\\",\\"source_oem\\":\\"NSP052601000Q1F\\",\\"source_rate\\":1,\\"stat_group\\":\\"0\\",\\"stat_group_type\\":\\"bad\\",\\"sup_logo\\":\\"12909\\",\\"sync_supplier_info\\":False,\\"visible_delivery_day\\":\\"1 день \\",\\"visible_sup_logo\\":\\"\\",\\"visible_sup_logo_www\\":\\"MP\\",\\"volume\\":\\"\\",\\"weight\\":3.3,\\"weightMethod\\":\\"api\\",\\"ws_raw_cost\\":8759.0,\\"ws_supplier_code\\":12909,\\"checkout_options\\":\\"None\\",\\"min_qnt\\":1}",
                    "supplier_order_item_id": None,
                    "qnt_accept": None,
                    "qnt_income": None,
                    "id_1c": "C224O573I688",
                    "min_delivery_day": 1,
                    "max_delivery_day": 1,
                    "add_in_ws": False,
                    "gtd": None,
                    "country": None,
                    "company_comment": None,
                    "delivery_comment": None,
                    "last_status_change_at": "2023-09-08T12:47:33.225 03:00",
                    "visible_order_id": 573, "customer_region_id": 1,
                    "user_name": "Сергей",
                    "status_code": "processing",
                    "customer_phone": " 7 (931) 252-81-57",
                    "customer_title": "Валерий (224)",
                    "customer_region_name": "Санкт-Петербург",
                    "price_region_name": "Санкт-Петербург",
                    "price_region_id": 1,
                    "last_status_notify": None,
                    "is_region_pair": False,
                    "region_order_item_id": None,
                    "order_complete_at": None,
                    "real_delivery_day": None,
                    "dialogs_count": 0,
                    "is_archive": False,
                    "external_order_id": None,
                    "external_order_type": None,
                    "ts_order_item_info": "\' 7\':151 \'-57\':155 \'-81\':154 \'/images/1554/14384427\':34 \'0\':104 \'1\':101,119,147 \'10248\':19 \'10702070/010520/0088963\':8 \'12909\':111,141 \'14\':7 \'15\':12 \'224\':156 \'24\':52,57 \'252\':153 \'2e1\':62 \'3.3\':131 \'4aa2\':66 \'573\':149 \'8759.0\':137 \'931\':152 \'a6d6\':65 \'api\':133 \'b0222a5f5c52\':68 \'bad\':108 \'bde1\':67 \'c224o573i688\':148 \'central\':13 \'checkout\':142 \'client\':16,20 \'code\':140 \'comment\':28,90,95 \'cost\':18,22,136 \'cross\':25 \'currenc\':23 \'day\':118 \'deliveri\':49,54,117 \'detail\':27 \'fals\':15,44,115 \'fdb71\':64 \'fdb71-a6d6-4aa2-bde1-b0222a5f5c52\':63 \'good\':29 \'group\':103,106 \'guid\':60 \'hide\':35 \'hour\':51,56 \'id\':61 \'img\':30 \'img-server-10.parts-soft.ru\':33 \'img-server-10.parts-soft.ru/images/1554/14384427\':32 \'info\':114 \'item\':45 \'key\':46 \'log\':70 \'logo\':38,110,123,126 \'make\':73,77 \'max\':48 \'min\':53,145 \'mp\':128 \'mpart\':10 \'name\':74,78 \'nissan\':5 \'None\':144 \'nsp\':2,75,79 \'nsp052601000q1f\':1,47,82,98 \'None\':71 \'oem\':43,81,97 \'option\':143 \'outdat\':42 \'price\':58,69 \'problem\':85,89 \'qnt\':146 \'rate\':100 \'raw\':72,135 \'request\':59,76,80 \'return\':83,87 \'rub\'"
                }
            ]
    }
}

tt = {'event_type': 'new_message',
      'payload': {'timestamp': 1694188853, 'msec_timestamp': 1694188853169, 'msgid': 'ca84673cd3fe5b43c00e0cdae08547ab',
                  'conversation_id': 'u2i-NYGSUv0QQ_0ZiJL~94eBJA',
                  'sender': {'id': 59108686, 'avatar': 'https://static.avito.ru/stub_avatars/_/14_256x256.png',
                             'profile': {'phone': '', 'email': ''},
                             'profile_link': 'https://avito.ru/user/97e2f94f0813176d08944ebd85cda862/profile?id=3364589989&iid=3364589989&src=messenger&page_from=from_item_messenger',
                             'name': 'Николай'}, 'message': {'type': 'text', 'text': 'Добрый вечер\nРейка в наличии?'},
                  'silent': False}}

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
                'updated_at': 1692957093, 'closed_at': 1692957093, 'closest_task_at': None, 'is_deleted': False,
                'custom_fields_values': None, 'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25767727?page=1&limit=20&order=created_at'}},
                '_embedded': {'tags': [], 'companies': []}},
            {'id': 25732023, 'name': 'Motorad 709-80/95K Термостат', 'price': 0, 'responsible_user_id': 9983934,
             'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0,
             'updated_by': 9983930, 'created_at': 1692797389, 'updated_at': 1692957242, 'closed_at': 1692957242,
             'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [
                {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                 'values': [{'value': 'Motorad 709-80/95K Термостат'}]},
                {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                 'values': [{
                     'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/motorad_709-8095k_termostat_3436678282'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25732023?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25697061, 'name': 'Mobiland 603100221 шрус наружный передний для а/м', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692794253,
             'updated_at': 1692957260, 'closed_at': 1692957260, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Mobiland 603100221 шрус наружный передний для а/м'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/mobiland_603100221_shrus_naruzhnyy_peredniy_dlya_am_3436591350'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25697061?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25478969, 'name': 'Ford 1447508 Подножка сдвижной двери. Transit TT9', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692618064,
             'updated_at': 1692973433, 'closed_at': 1692973433, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Ford 1447508 Подножка сдвижной двери. Transit TT9'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/ford_1447508_podnozhka_sdvizhnoy_dveri._transit_tt9_3403943407'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25478969?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25761021, 'name': 'Zimmermann 290.2264.52 Торм.диск пер.вент.355x32 5', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692797978,
             'updated_at': 1693235863, 'closed_at': 1693235863, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Zimmermann 290.2264.52 Торм.диск пер.вент.355x32 5'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/zimmermann_290.2264.52_torm.disk_per.vent.355x32_5_3435853015'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25761021?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25735957, 'name': 'Luzar lric 0801 Интеркулер', 'price': 0, 'responsible_user_id': 9983934,
             'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0,
             'updated_by': 9983930, 'created_at': 1692797478, 'updated_at': 1693235943, 'closed_at': 1693235943,
             'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [
                {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                 'values': [{'value': 'Luzar lric 0801 Интеркулер'}]},
                {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                 'values': [{
                     'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/luzar_lric_0801_interkuler_3435816856'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25735957?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25650247, 'name': 'Miles BLC0016 Высоковольтные провода зажигания for', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692728554,
             'updated_at': 1693235961, 'closed_at': 1693235961, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Miles BLC0016 Высоковольтные провода зажигания for'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/miles_blc0016_vysokovoltnye_provoda_zazhiganiya_for_3436472985'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25650247?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25650847, 'name': 'Miles GA10048 шрус toyota avensis T220/T250/coroll', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692731228,
             'updated_at': 1693235988, 'closed_at': 1693235988, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Miles GA10048 шрус toyota avensis T220/T250/coroll'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/miles_ga10048_shrus_toyota_avensis_t220t250coroll_3436658919'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25650847?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25574249, 'name': 'Gates TH35991 Термостат охлаждающей жидкости', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692715257,
             'updated_at': 1693236018, 'closed_at': 1693236018, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Gates TH35991 Термостат охлаждающей жидкости'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/gates_th35991_termostat_ohlazhdayuschey_zhidkosti_3436062523'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25574249?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25573403, 'name': 'Airline aprd04 Манометр цифровой ЖК дисплей 7 атм', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692713464,
             'updated_at': 1693236166, 'closed_at': 1693236166, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Airline aprd04 Манометр цифровой ЖК дисплей 7 атм'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/airline_aprd04_manometr_tsifrovoy_zhk_displey_7_atm_3403708811'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25573403?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25567837, 'name': 'BMW 17137639023 Пробка радиатора', 'price': 0, 'responsible_user_id': 9983934,
             'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0,
             'updated_by': 9983930, 'created_at': 1692709715, 'updated_at': 1693236184, 'closed_at': 1693236184,
             'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [
                {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                 'values': [{'value': 'BMW 17137639023 Пробка радиатора'}]},
                {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                 'values': [{
                     'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/bmw_17137639023_probka_radiatora_3404627392'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25567837?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25562093, 'name': 'Chrysler 68188865AA клапан вентиляции картера', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692704921,
             'updated_at': 1693236197, 'closed_at': 1693236197, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Chrysler 68188865AA клапан вентиляции картера'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/chrysler_68188865aa_klapan_ventilyatsii_kartera_3403834953'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25562093?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25545157, 'name': 'KYB 341851 Амортизатор подвески задний', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692695462,
             'updated_at': 1693236282, 'closed_at': 1693236282, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'KYB 341851 Амортизатор подвески задний'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/kyb_341851_amortizator_podveski_zadniy_3436109485'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25545157?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25541891, 'name': 'General motors 93160377 антифриз', 'price': 0, 'responsible_user_id': 9983934,
             'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526, 'loss_reason_id': None, 'created_by': 0,
             'updated_by': 9983930, 'created_at': 1692690902, 'updated_at': 1693236325, 'closed_at': 1693236325,
             'closest_task_at': None, 'is_deleted': False, 'custom_fields_values': [
                {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                 'values': [{'value': 'General motors 93160377 антифриз'}]},
                {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                 'values': [{
                     'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/general_motors_93160377_antifriz_3436667992'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25541891?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25510385, 'name': 'Fenox CTC3504 Суппорт Mitsubishi Lancer viii (CX,C', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983930, 'created_at': 1692647363,
             'updated_at': 1693236401, 'closed_at': 1693236401, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Fenox CTC3504 Суппорт Mitsubishi Lancer viii (CX,C'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/fenox_ctc3504_support_mitsubishi_lancer_viii_cxc_3403742739'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25510385?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25655535, 'name': 'VAG 5K0698451E Колодки тормозные дисковые', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983934, 'created_at': 1692768333,
             'updated_at': 1693307107, 'closed_at': 1693307107, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'VAG 5K0698451E Колодки тормозные дисковые'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/vag_5k0698451e_kolodki_tormoznye_diskovye_3435728746'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25655535?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25693609, 'name': 'Teknorot B10182 Рычаг подвески BMW 5 серия G30, F9', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 9983934, 'created_at': 1692789524,
             'updated_at': 1693317506, 'closed_at': 1693317506, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Teknorot B10182 Рычаг подвески BMW 5 серия G30, F9'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/teknorot_b10182_rychag_podveski_bmw_5_seriya_g30_f9_3435875736'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25693609?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}},
            {'id': 25955555, 'name': 'Polmostrow 1003AL P10.03AL глушитель средняя часть', 'price': 0,
             'responsible_user_id': 9983934, 'group_id': 0, 'status_id': 143, 'pipeline_id': 7155526,
             'loss_reason_id': None, 'created_by': 0, 'updated_by': 0, 'created_at': 1692987860,
             'updated_at': 1693331350, 'closed_at': 1693306038, 'closest_task_at': None, 'is_deleted': False,
             'custom_fields_values': [
                 {'field_id': 987783, 'field_name': 'Объявление', 'field_code': None, 'field_type': 'text',
                  'values': [{'value': 'Polmostrow 1003AL P10.03AL глушитель средняя часть'}]},
                 {'field_id': 987785, 'field_name': 'URL объявления', 'field_code': None, 'field_type': 'url',
                  'values': [{
                      'value': 'https://avito.ru/sankt-peterburg/zapchasti_i_aksessuary/polmostrow_1003al_p10.03al_glushitel_srednyaya_chast_3435821014'}]}],
             'score': None, 'account_id': 31247590, 'labor_cost': None, '_links': {
                'self': {'href': 'https://amo3431ru.amocrm.ru/api/v4/leads/25955555?page=1&limit=20&order=created_at'}},
             '_embedded': {'tags': [], 'companies': []}}]}}

ss = {"account_id": "af9945ff-1490-4cad-807d-945c15d88bec", "title": "ScopeTitle", "hook_api_version": "v2"}

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


def check_price(row):
    check, k = False, 1
    nacenka = int(row[4]) / int(row[3])
    if 0 < row[3] <= 1500:
        k = 1.5
        if nacenka >= 1.5:
            check = True

    elif 1501 <= row[3] <= 3000:
        k = 1.4
        if nacenka >= 1.4:
            check = True

    elif 3001 <= row[3]:
        k = 1.36
        if nacenka >= 1.36:
            check = True

    return check, nacenka, k


import openpyxl


def read_sales_v2(sales):
    proxy, faxy, maxy = [], {}, []

    data = pd.read_excel(sales)
    df = pd.DataFrame(data).values
    for row in df:
        check = check_price(list(row))
        if check[0]:
            continue
        else:
            price = int(row[3]) * check[2]
            print(price, check)
            try:
                # faxy = [row[0], row[1], row[2], row[3], row[4], row[5], price, int(row[45])]
                faxy = [row[0], row[1], row[2], row[3], row[4], price, check[1], check[2], int(row[45])]
                print(faxy)
                proxy.append(faxy)
            except:
                continue
        # print(row)
        # print(check)
        print(len(proxy))
        # print(list(row).index(5372))

    df = pd.DataFrame(proxy,
                      # index=['one', 'two', 'three'],
                      columns=['артикул', 'Бренд', 'Название', 'Закупка',
                               'Продажа', 'Цена по ТЗ', 'Наценка',
                               'Наценка по ТЗ', 'Отправление'])
    df.to_excel('./pandas_proxy_data.xlsx', index=False)

    # os.abort()

    print('result', len(faxy))
    with open("./proxy_data.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(proxy)


one = [9821121088694, 9843956888810, 9737058339086, 9737058339086, 9803649831314, 9803649831314, 9765477642866,
       9765477642866, 9757914367478, 9746592262826, 9721466496338, 9645733385366, 9566314432106, 9587918577002,
       9575921342822, 9549290219954, 9508408390022, 9451852606994, 9477242951270, 9473566232354, 9375353132774,
       9437601899930, 9437282581910, 9421626875558, 9409383310334, 9360555023390, 9302621611190, 9311434788542,
       9312867157946, 9317967122894, 9338978248610, 9249277255106, 9280132499210, 9290022234458, 9209608833650,
       9238867487654, 9231860737958, 9168261711746, 9190458875822, 9163262103890, 9158992365794, 9076389355706,
       9068442898694, 9133747995470, 9073442506550, 9125710304738, 9003940658654, 9048690798314, 9976898984035,
       9975238530331, 9037295706686, 9990730015987, 9958031850739, 9956207176339, 9958944187939, 9958944187939,
       9958944187939, 9955741884367, 9937093711999, 9919485604039, 9860749335103, 9896321362531, 9885063121483,
       9873403452067, 9873403452067, 9857775115831, 9788410118515, 9749371209727, 9813271307215, 9818006337283,
       9746196276271, 9750703222039, 9676530207679, 9676530207679, 9668720601247, 9722968171159, 9722968171159,
       9640036719679, 9606398847115, 9606398847115, 9627674550619, 9627674550619, 9678573843007, 9678573843007,
       9563528122087, 9530218690915, 9591108075643, 9532691124727, 9494208741631, 9526551095371, 9543557060779,
       9538913264431, 9515283730951, 9504080230135, 9502611367243, 9456209897251, 9424697770363, 9463955640079,
       9463955640079, 9472449499411, 9385056719023, 9447624804199, 9351847644943, 9373725490999, 9383049577183,
       9340817488195, 9327944410303, 9328336715299, 9209933593483, 9209933593483, 9209933593483, 9209933593483,
       9209933593483, 9205098206323, 9237513547039, 9039490757779, 9162802253731, 9082507456759, 9013507394323,
       9010295967379, 9999594252012, 9049937018719, 9012366972823, 9942299475852, 9933486298500, 9933486298500,
       9876702431172, 9926780620080, 9926780620080, 9926780620080, 9914527931484, 9828686124336, 9819918563844,
       9818175999792, 9825702781692, 9774931216512, 9774931216512, 9774931216512, 9851987216424, 9813705547512,
       9813085158216, 9704334563976, 9713047384236, 9710611443912, 9703778038284, 9674190942888, 9643390439016,
       9635298008052, 9641866835892, 9581816801388, 9477043997340, 9514632289980, 9442220086416, 9436682199612,
       9432987233952, 9424648471944, 9368412006936, 9380901903204, 9394669071552, 9280006532256, 9315578559684,
       9298727691600, 9314036709816, 9261394853376, 9240967623468, 9236259963516, 9236259963516, 9219701043336,
       9201682383636, 9185953690308, 9177122266212, 9942624235685, 9101279674776, 9131560146444, 9062158655640,
       9062988882492, 9112610902800, 9037799252400, 9980020937513, 9029715944808, 9975586978721, 9921385025669,
       9638469259949, 9840469839401, 9862730867081, 9874837581725, 9854054540309, 9879353650865, 9876844723565,
       9876844723565, 9871580537921, 9805016415809, 9803720896985, 9800418236321, 9840843897653, 9789415449689,
       9724657755233, 9744948134561, 9740058007169, 9676112292821, 9650457370757, 9685710080165, 9681942127529,
       9610268917097, 9589695713237, 9639600558077, 9585654059441, 9616162615409, 9616162615409, 9567069750677,
       9582734580401, 9529782529313, 9578574322769, 9564287122217, 9575390265941, 9575390265941, 9556641736481,
       9519463995581, 9487796771369, 9438229491293, 9484922909189, 9456932403893, 9393543215237, 9420365928917,
       9404400027917, 9393269514077, 9355818072017, 9349933497077, 9292894175333, 9314744651273, 9264100813301,
       9225609306833, 9193157472629, 9175129689557, 9175129689557, 9104624270741, 9103201024709, 9083129606309,
       9025634115965, 9069371561333, 9875965198294, 9854096475610, 9208973718118]
two = [9705042666484, 9696749521336, 9682799885548, 9682799885548, 9674479370284, 9587004479548, 9654261977932,
       9690080336404, 9596866844680, 9649782402280, 9618598716784, 9608490020608, 9561687122248, 9493654137244,
       9516380456896, 9516380456896, 9494831052232, 9545648234272, 9521124610336, 9448411335496, 9444141597400,
       9394236752560, 9392767889668, 9369275206768, 9358938426292, 9325920943024, 9587389421426, 9538287433322,
       9530924872118, 9451469425370, 9417813306062, 9210083248994, 9203185979762, 9202301012678, 9178352161178,
       9032907364754, 9896293992415, 9597430572439, 9635584514143, 9488543127619, 9448509771283, 9463928269963,
       9442378865299, 9406122584971, 9384034901359, 9321603666763, 9365733417127, 9356336343967, 9324523145803,
       9213053786707, 9252074448751, 9869330746596, 9926753249964, 9840902319444, 9883353369360, 9764968494288,
       9708020406264, 9524950823712, 9561772753104, 9554893730616, 9599370169116, 9567693821532, 9491267334288,
       9477773867100, 9437275218792, 9361250159916, 9332785239276, 9312987522036, 9217246856268, 9247244503404,
       9180871972104, 9025181628924, 9074967869928, 9060315734496, 9803693526869, 9328785520781, 9213493468817,
       9086505253949, 9134010651953, 9049747188161, 9044063327405, 9046690858541, 9009951039497, 9012888765281,
       9979296509566, 9970291741402, 9897487232842, 9897487232842, 9831589116886, 9819382045150, 9420416987590,
       9472133701899, 9472133701899]

tree = [9717140257756, 9712835786426, 9717525199634, 9719203900082, 9662401786010, 9644072931662, 9650751239966,
        9634958683034, 9636053487674, 9604285906370, 9533287825466, 9540294575162, 9504676930874, 9477908957426,
        9403872793646, 9399657795782, 9378801767390, 9337527632462, 9285506165318, 9312064301210, 9312064301210,
        9223613209670, 9271392308834, 9196033256114, 9254413713542, 9208514029010, 9228393856598, 9122489754422,
        9116431835414, 9079682892998, 9046473818918, 9023127109970, 9018200489090, 9956900552611, 9924831900031,
        9805790142175, 9800772287575, 9827950812763, 9746734555219, 9810680269567, 9807286375183, 9807286375183,
        9756779387791, 9703407661591, 9690178772191, 9694594484239, 9676320370123, 9644333827891, 9650327883295,
        9606271119907, 9608624949883, 9597987098131, 9494345592211, 9588453174391, 9549414265603, 9478315827607,
        9511543148431, 9509107208107, 9426403840927, 9389153113051, 9382210226959, 9427270561267, 9381553344175,
        9308174063179, 9285967775731, 9327251034031, 9250541722255, 9292345012759, 9286670275375, 9213555572167,
        9160840728751, 9203218791691, 9131499964399, 9176323091035, 9967324885248, 9077553465763, 9054307113907,
        9977369717820, 9956075767572, 9020422910299, 9012339602707, 9889593755808, 9959396674980, 9959396674980,
        9860955491100, 9828357682944, 9813869768208, 9770615861556, 9802228345536, 9779994687972, 9584663293452,
        9598959617376, 9513701706036, 9570887001732, 9500171745360, 9486413700384, 9557411781288, 9548489123472,
        9503109471144, 9503109471144, 9378310865556, 9368384636820, 9415515976572, 9340029196644, 9338140658640,
        9359872530744, 9295935939768, 9343596435096, 9258520991196, 9281548382124, 9251350020804, 9251350020804,
        9241104474048, 9226388475012, 9222565782144, 9252691156488, 9217557050916, 9204309914772, 9253658233920,
        9193234141164, 9234033860748, 9234033860748, 9098761624104, 9172396359516, 9080615237196, 9103487530800,
        9038383148208, 9086846500272, 9085176923196, 9075387545040, 9011332350228, 9011332350228, 9951391796177,
        9951391796177, 9927251353865, 9875166023117, 9876817353449, 9865860183677, 9819011668457, 9771661367777,
        9789388079573, 9789388079573, 9789388079573, 9725387624993, 9725387624993, 9685299528425, 9689249948501,
        9674360605397, 9664206292361, 9664206292361, 9641616823289, 9648687436589, 9678475246169, 9637064260661,
        9580170912869, 9561376766549, 9564259752101, 9562161376541, 9562161376541, 9560455305977, 9557617937285,
        9485552421857, 9459176753405, 9483654760481, 9477560347985, 9473637298025, 9438950237681, 9420338558801,
        9376993418429, 9292866805217, 9271317400553, 9317591143337, 9296479660529, 9296552647505, 9288597067121,
        9242843356541, 9280185318137, 9244969102217, 9238144819961, 9162512066081, 9143416848485, 9149474767493,
        9151536649565, 9092937231209, 9120024522677, 9037038330965, 9000800297381]

returning = [9000800297381, 9009951039497, 9011332350228, 9011332350228, 9011332350228, 9012339602707, 9012888765281,
             9018200489090, 9020422910299, 9023127109970, 9025181628924, 9032907364754, 9032907364754, 9032907364754,
             9037038330965, 9038383148208, 9044063327405, 9046473818918, 9046690858541, 9048727291802, 9049747188161,
             9054307113907, 9060315734496, 9074967869928, 9075387545040, 9077553465763, 9079682892998, 9080166431714,
             9080166431714, 9080615237196, 9085176923196, 9086505253949, 9086846500272, 9092937231209, 9098761624104,
             9102735732737, 9103487530800, 9106549302233, 9106549302233, 9116431835414, 9120024522677, 9120382255490,
             9122489754422, 9131499964399, 9134010651953, 9143416848485, 9145157652283, 9149474767493, 9151536649565,
             9160840728751, 9162512066081, 9172040548008, 9172396359516, 9176323091035, 9178352161178, 9180871972104,
             9191991602318, 9193234141164, 9196033256114, 9202301012678, 9203185979762, 9203185979762, 9203185979762,
             9203185979762, 9203218791691, 9204309914772, 9208514029010, 9210083248994, 9213053786707, 9213493468817,
             9213555572167, 9217246856268, 9217557050916, 9222565782144, 9223613209670, 9226388475012, 9228393856598,
             9234033860748, 9234033860748, 9238144819961, 9241104474048, 9242843356541, 9244969102217, 9247244503404,
             9250541722255, 9251350020804, 9251350020804, 9252074448751, 9252691156488, 9253658233920, 9254413713542,
             9258520991196, 9266735707555, 9270886841815, 9271317400553, 9271392308834, 9280185318137, 9281548382124,
             9285506165318, 9285967775731, 9286670275375, 9288597067121, 9292345012759, 9292866805217, 9295935939768,
             9296479660529, 9296552647505, 9308174063179, 9309650128138, 9312064301210, 9312064301210, 9312987522036,
             9317591143337, 9321603666763, 9324523145803, 9325920943024, 9327251034031, 9328785520781, 9332785239276,
             9337527632462, 9338140658640, 9340029196644, 9343596435096, 9356336343967, 9359872530744, 9361250159916,
             9365733417127, 9368384636820, 9376993418429, 9378310865556, 9378801767390, 9381553344175, 9382210226959,
             9384034901359, 9389153113051, 9389153113051, 9399657795782, 9403872793646, 9406122584971, 9415515976572,
             9417813306062, 9417813306062, 9417813306062, 9420338558801, 9420416987590, 9426403840927, 9427270561267,
             9437275218792, 9438950237681, 9442378865299, 9448509771283, 9451469425370, 9459176753405, 9463928269963,
             9466856872375, 9472133701899, 9472133701899, 9472133701899, 9473637298025, 9477560347985, 9477773867100,
             9477908957426, 9478315827607, 9483654760481, 9485552421857, 9485901031298, 9486413700384, 9488543127619,
             9491267334288, 9494345592211, 9495942182311, 9500171745360, 9503109471144, 9503109471144, 9504676930874,
             9504676930874, 9509107208107, 9511543148431, 9513701706036, 9524950823712, 9530924872118, 9533287825466,
             9538287433322, 9540294575162, 9548489123472, 9549414265603, 9554893730616, 9557411781288, 9557617937285,
             9560455305977, 9560586714744, 9561376766549, 9561772753104, 9562161376541, 9562161376541, 9564259752101,
             9567693821532, 9570887001732, 9572122338511, 9580170912869, 9584663293452, 9587389421426, 9588453174391,
             9597430572439, 9597987098131, 9598959617376, 9599370169116, 9599370169116, 9604285906370, 9606271119907,
             9608624949883, 9620041808763, 9634925710054, 9634925710054, 9634958683034, 9635584514143, 9636053487674,
             9637064260661, 9637064260661, 9641616823289, 9644072931662, 9644333827891, 9648687436589, 9650327883295,
             9650751239966, 9662401786010, 9664206292361, 9664206292361, 9674360605397, 9676320370123, 9678475246169,
             9682721295708, 9685299528425, 9686458357720, 9689249948501, 9690178772191, 9694594484239, 9694740458191,
             9702353031998, 9703407661591, 9708020406264, 9712835786426, 9717140257756, 9717525199634, 9719203900082,
             9719959379704, 9725387624993, 9725387624993, 9746734555219, 9756779387791, 9764968494288, 9770615861556,
             9770615861556, 9771661367777, 9779994687972, 9789388079573, 9789388079573, 9789388079573, 9789652657361,
             9795544595419, 9800772287575, 9802228345536, 9803693526869, 9805790142175, 9807286375183, 9807286375183,
             9810680269567, 9813869768208, 9819011668457, 9819382045150, 9826755651031, 9826755651031, 9827950812763,
             9828357682944, 9831589116886, 9840902319444, 9860955491100, 9865860183677, 9869330746596, 9875166023117,
             9876817353449, 9876817353449, 9883353369360, 9889593755808, 9896293992415, 9896293992415, 9897487232842,
             9897487232842, 9897487232842, 9924831900031, 9926753249964, 9927251353865, 9951391796177, 9951391796177,
             9956075767572, 9956900552611, 9959396674980, 9959396674980, 9967324885248, 9970291741402, 9977369717820,
             9979296509566]
returning2 = [9003940658654, 9010295967379, 9012366972823, 9012366972823, 9013507394323, 9025634115965, 9028345517703,
              9029715944808, 9037295706686, 9037799252400, 9039490757779, 9039490757779, 9043483113156, 9048690798314,
              9049937018719, 9062158655640, 9062988882492, 9068442898694, 9069371561333, 9073442506550, 9076389355706,
              9082507456759, 9083129606309, 9094942612795, 9101279674776, 9103201024709, 9104624270741, 9112610902800,
              9125710304738, 9131560146444, 9133747995470, 9158992365794, 9162802253731, 9163262103890, 9168261711746,
              9175129689557, 9175129689557, 9177122266212, 9185953690308, 9190458875822, 9193157472629, 9201682383636,
              9205098206323, 9208973718118, 9209608833650, 9209933593483, 9209933593483, 9209933593483, 9209933593483,
              9209933593483, 9213586623842, 9213586623842, 9219701043336, 9225609306833, 9231860737958, 9233473653497,
              9236259963516, 9236259963516, 9236259963516, 9237513547039, 9238867487654, 9240967623468, 9253397337691,
              9261394853376, 9261394853376, 9264100813301, 9280006532256, 9292894175333, 9298727691600, 9314036709816,
              9314744651273, 9315578559684, 9315578559684, 9327944410303, 9327944410303, 9327944410303, 9328336715299,
              9340817488195, 9349933497077, 9351847644943, 9355818072017, 9368412006936, 9373725490999, 9380901903204,
              9381027870158, 9383049577183, 9385056719023, 9386963503771, 9386963503771, 9393269514077, 9393543215237,
              9394669071552, 9400159581242, 9400159581242, 9404400027917, 9420365928917, 9424648471944, 9424697770363,
              9432987233952, 9436682199612, 9438229491293, 9442220086416, 9447624804199, 9456209897251, 9456932403893,
              9463955640079, 9463955640079, 9472449499411, 9477043997340, 9483466851228, 9484922909189, 9485928401414,
              9487796771369, 9494208741631, 9502611367243, 9504080230135, 9514632289980, 9515283730951, 9519463995581,
              9526551095371, 9529782529313, 9530218690915, 9532691124727, 9538913264431, 9542493307814, 9543557060779,
              9556641736481, 9563528122087, 9564287122217, 9567069750677, 9575390265941, 9575390265941, 9578574322769,
              9581816801388, 9582734580401, 9585654059441, 9589695713237, 9591108075643, 9606398847115, 9606398847115,
              9610268917097, 9616162615409, 9616162615409, 9627674550619, 9627674550619, 9627674550619, 9635298008052,
              9638469259949, 9639600558077, 9640036719679, 9641866835892, 9643390439016, 9647649293486, 9650457370757,
              9668720601247, 9670683886481, 9671722190635, 9671722190635, 9674190942888, 9676112292821, 9676530207679,
              9676530207679, 9678573843007, 9678573843007, 9681942127529, 9685710080165, 9689494358240, 9703778038284,
              9704334563976, 9710611443912, 9713047384236, 9722968171159, 9722968171159, 9724657755233, 9740058007169,
              9744101582270, 9744948134561, 9746196276271, 9749371209727, 9750703222039, 9774931216512, 9774931216512,
              9774931216512, 9788410118515, 9789415449689, 9793869576530, 9800418236321, 9803720896985, 9805016415809,
              9813085158216, 9813271307215, 9813705547512, 9818006337283, 9818175999792, 9819918563844, 9825702781692,
              9828686124336, 9840469839401, 9840843897653, 9843956888810, 9851987216424, 9854054540309, 9854096475610,
              9857775115831, 9860749335103, 9860749335103, 9862730867081, 9871580537921, 9871580537921, 9873403452067,
              9873403452067, 9874837581725, 9875965198294, 9876702431172, 9876844723565, 9876844723565, 9879353650865,
              9885063121483, 9896321362531, 9914527931484, 9919485604039, 9921385025669, 9926780620080, 9926780620080,
              9926780620080, 9933486298500, 9933486298500, 9937093711999, 9942299475852, 9942299475852, 9942624235685,
              9955741884367, 9956207176339, 9957553592785, 9958031850739, 9958944187939, 9958944187939, 9958944187939,
              9975238530331, 9975586978721, 9976898984035, 9980020937513, 9990730015987, 9999594252012]


def check_exist(row):
    try:
        if str(row[12]) != 'nan' and int(row[45]) and (int(row[45]) in returning or int(row[45]) in returning2):
            print(1333333333333, row[12], row)
            return True
        else:
            print(111111111, row[12], row)
            return False
    except:
        print(12222222221, row[12], row)


def read_sales_v3(sales):
    proxy, faxy, maxy = [], {}, []

    data = pd.read_excel(sales)
    df = pd.DataFrame(data).values
    for row in df:
        # print(row)
        check = check_exist(list(row))
        # print(list(row).index('СБЕРМАРКЕТ (710)'))
        # os.abort()
        if not check:
            continue
        else:
            try:
                faxy = [row[0], row[1], row[2], row[12], row[13], int(row[45])]
                # print(faxy)
                proxy.append(faxy)
            except:
                continue
        # print(row)
        # print(check)
        print(len(proxy))
        # print(list(row).index(5372))

    df = pd.DataFrame(proxy,
                      # index=['one', 'two', 'three'],
                      columns=['артикул', 'Бренд', 'Название',
                               'поставщик', 'маркетплейс', 'Отправление'])
    df.to_excel('./pandas_proxy_data-1.xlsx', index=False)


# read_sales('order_items_28_02_2.xls', 'price_rew.xls')
# read_sales_v3('./order_items_all.xls')
#
# extract_phone_number_pattern = "\\+?[7-9][0-9]{9,11}"
# stringg = "8,9,2,8,3,6,2,6,4,6,5 \
#       будьте добрый свяжитесь с нами , что мы мы могли поговорить о сотрудничестве"
# #'Семь 9172213870' # 'Алпацкий Денис Юрьевич. Город Хабаровск,ул. Сысоева, дом 2, КВ. 20. 8 962 500 94 98. Отправить почтой РФ первым классом.'
# strrr = stringg.replace(',', '')
# print(re.findall(extract_phone_number_pattern, strrr))
#
# print(strrr)
# fack = {'account_id': '5a963077-682d-424d-a923-b5fe95b27a8e', 'time': 1710230849, 'message': {
#     'receiver': {'id': '4c44b607-e14b-438d-8eaf-afbeac69e259', 'name': 'Илья Мельников', 'client_id': '97699016'},
#     'sender': {'id': 'e9190cc9-dbd8-4815-8f33-4c4e8f1a66aa', 'name': 'Менеджер4'},
#     'conversation': {'id': 'b9c61188-bb73-4fd1-8b20-c9a22bc05a54', 'client_id': 'u2i-AL2UQTMwlPz8uVjn64OIhQ'},
#     'timestamp': 1710230849, 'msec_timestamp': 1710230849023,
#     'message': {'id': '01a37eeb-5896-463a-a4a3-db86790db00a', 'type': 'text',
#                 'text': 'Добрый день! видео отправили, крепления целые, напишите номер, вотс апп Вам видео отправлю',
#                 'markup': None, 'tag': '', 'media': '', 'thumbnail': '', 'file_name': '', 'file_size': 0}}}
#

def load(dt):
    header = {'X-Avito-Messenger-Signature': ''}
    url = 'https://phone-call.i-bots.ru/webhook'
    answer = requests.post(url, data=dt, headers=header)

    print(answer.text)


# load(fack)

# data = json.loads("""{ "entry":{ "etag":"W/\\"A0UGRK47eCp7I9B9WiRrYU0.\\"" } }""")
# data = json.dumps({'id': '75e58e8e-bfa1-403d-8056-6c6c792cf7eb', 'version': 'v3.0.0', 'timestamp': 1710334363, 'payload': {'type': 'message', 'value': {'id': '06e9a846e3959dcd148ca7d507957f90', 'chat_id': 'u2i-edoS30kaZhxk~xihAdJ8Ow', 'user_id': 369222251, 'author_id': 369222251, 'created': 1710334362, 'type': 'text', 'chat_type': 'u2i', 'content': {'text': 'Добрый день.\n Благодарим за Ваше обращение в нашу компанию. Ваша заявка получена и наш специалист скоро свяжется с Вами. Если Вы хотите ускорить процесс - отправьте нам: \n Как к Вам можно обращаться (фио) \n Номер телефона \n VIN или артикул или название детали\n и Ваша заявка сразу попадёт в работу.'}, 'item_id': 3689394459}}})
# data = json.dumps({'id': '75e58e8e-bfa1-403d-8056-6c6c792cf7eb', 'version': 'v3.0.0', 'timestamp': 1710334363, 'payload': {'type': 'message', 'value': {'id': '06e9a846e3959dcd148ca7d507957f90', 'chat_id': 'u2i-edoS30kaZhxk~xihAdJ8Ow', 'user_id': 369222251, 'author_id': 369222251, 'created': 1710334362, 'type': 'text', 'chat_type': 'u2i', 'content': {'text': 'Добрый день.\\n Благодарим за Ваше обращение в нашу компанию. Ваша заявка получена и наш специалист скоро свяжется с Вами. Если Вы хотите ускорить процесс - отправьте нам: \\n Как к Вам можно обращаться (фио) \\n Номер телефона \\n VIN или артикул или название детали\\n и Ваша заявка сразу попадёт в работу.'}, 'item_id': 3689394459}}})

# print(data)

respose_ym = {
    "pager": {
        "total": 7, "from": 1, "to": 7, "currentPage": 1, "pagesCount": 1, "pageSize": 50}, "orders": [
        {"id": 451642783, "status": "PROCESSING", "substatus": "STARTED", "creationDate": "02-05-2024 11:37:27",
         "currency": "RUR", "itemsTotal": 6772.0, "deliveryTotal": 0.0, "buyerItemsTotal": 6772.0, "buyerTotal": 6772.0,
         "buyerItemsTotalBeforeDiscount": 7524.0, "buyerTotalBeforeDiscount": 7524.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591932346, "offerId": "STELLOX42140459SX",
                                                              "offerName": "STELLOX 42140459SX 4214-0459-SX_\u0430\u043c\u043e\u0440\u0442\u0438\u0437\u0430\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u0434\u043d\u0438\u0439 \u0433\u0430\u0437\u043e\u0432\u044b\u0439!\\ BMW E39 2.0-3.0/2.5TD/3.0D 95",
                                                              "price": 3386.0, "buyerPrice": 3386.0,
                                                              "buyerPriceBeforeDiscount": 3762.0,
                                                              "priceBeforeDiscount": 3762.0, "count": 2,
                                                              "vat": "NO_VAT", "shopSku": "STELLOX42140459SX",
                                                              "subsidy": 376.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                                                              "promos": [
                                                                  {"type": "MARKET_PROMOCODE", "subsidy": 376.0}],
                                                              "subsidies": [{"type": "SUBSIDY", "amount": 376.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 752.0}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "16-05-2024", "toDate": "18-05-2024", "fromTime": "09:00:00",
                                "toTime": "18:00:00"},
                      "region": {"id": 11314, "name": "\u0411\u0435\u0440\u0434\u0441\u043a", "type": "CITY",
                                 "parent": {"id": 121038,
                                            "name": "\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0411\u0435\u0440\u0434\u0441\u043a",
                                            "type": "REPUBLIC_AREA", "parent": {"id": 11316,
                                                                                "name": "\u041d\u043e\u0432\u043e\u0441\u0438\u0431\u0438\u0440\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                "type": "REPUBLIC", "parent": {"id": 59,
                                                                                                               "name": "\u0421\u0438\u0431\u0438\u0440\u0441\u043a\u0438\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                               "type": "COUNTRY_DISTRICT",
                                                                                                               "parent": {
                                                                                                                   "id": 225,
                                                                                                                   "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                                   "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "633009",
                                  "city": "\u0411\u0435\u0440\u0434\u0441\u043a",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 \u041a\u0440\u0430\u0441\u043d\u0430\u044f \u0421\u0438\u0431\u0438\u0440\u044c",
                                  "gps": {"latitude": 54.746995, "longitude": 83.058739}}, "deliveryServiceId": 632848,
                      "liftPrice": 0.0, "outletCode": "28568", "shipments": [
                 {"id": 446332169, "shipmentDate": "08-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567463109, "fulfilmentId": "451642783-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": False},
        {"id": 451638056, "status": "CANCELLED", "substatus": "CUSTOM", "creationDate": "02-05-2024 11:27:13",
         "currency": "RUR", "itemsTotal": 4643.0, "deliveryTotal": 0.0, "buyerItemsTotal": 4643.0, "buyerTotal": 4643.0,
         "buyerItemsTotalBeforeDiscount": 4690.0, "buyerTotalBeforeDiscount": 4690.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591927025, "offerId": "TRIALLIGT990",
                                                              "offerName": "TRIALLI GT990 \u0420\u0435\u043c\u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442 \u0413\u0420\u041c \u0434\u043b\u044f \u0430/\u043c \u041b\u0430\u0434\u0430 Granta (10-) 8V (\u043f\u043e\u043c\u043f\u0430Luzar/\u0440\u0435\u043c\u0435\u043d\u044c/1 \u0440\u043e\u043b\u0438\u043a) (GT 990)",
                                                              "price": 4643.0, "buyerPrice": 4643.0,
                                                              "buyerPriceBeforeDiscount": 4690.0,
                                                              "priceBeforeDiscount": 4690.0, "count": 1,
                                                              "vat": "NO_VAT", "shopSku": "TRIALLIGT990",
                                                              "subsidy": 47.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                                                              "subsidies": [{"type": "SUBSIDY", "amount": 47.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 47.0}],
         "delivery": {"type": "DELIVERY", "serviceName": "\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "13-05-2024", "toDate": "13-05-2024", "fromTime": "10:00:00",
                                "toTime": "23:00:00"}, "region": {"id": 54,
                                                                  "name": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                                                  "type": "CITY", "parent": {"id": 121110,
                                                                                             "name": "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u043e\u0435 \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                                                                             "type": "REPUBLIC_AREA",
                                                                                             "parent": {"id": 11162,
                                                                                                        "name": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                                        "type": "REPUBLIC",
                                                                                                        "parent": {
                                                                                                            "id": 52,
                                                                                                            "name": "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0438\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                            "type": "COUNTRY_DISTRICT",
                                                                                                            "parent": {
                                                                                                                "id": 225,
                                                                                                                "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                                "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                  "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 \u041a\u0443\u043b\u044c\u0442\u0443\u0440\u044b",
                                  "house": "25", "gps": {"latitude": 56.890663, "longitude": 60.574873}},
                      "deliveryServiceId": 78080, "liftPrice": 0.0, "shipments": [
                 {"id": 446327442, "shipmentDate": "08-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567459587, "fulfilmentId": "451638056-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": True},
        {"id": 451603539, "status": "PROCESSING", "substatus": "STARTED", "creationDate": "02-05-2024 10:08:02",
         "currency": "RUR", "itemsTotal": 2689.0, "deliveryTotal": 0.0, "buyerItemsTotal": 2689.0, "buyerTotal": 2689.0,
         "buyerItemsTotalBeforeDiscount": 2716.0, "buyerTotalBeforeDiscount": 2716.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591888087, "offerId": "DEPO5512004LUE",
                                                              "offerName": "DEPO 551-2004L-UE \u0424\u0430\u0440\u0430 \u043f\u0440\u043e\u0442\u0438\u0432\u043e\u0442\u0443\u043c\u0430\u043d\u043d\u0430\u044f L",
                                                              "price": 2689.0, "buyerPrice": 2689.0,
                                                              "buyerPriceBeforeDiscount": 2716.0,
                                                              "priceBeforeDiscount": 2716.0, "count": 1,
                                                              "vat": "NO_VAT", "shopSku": "DEPO5512004LUE",
                                                              "subsidy": 27.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                                                              "subsidies": [{"type": "SUBSIDY", "amount": 27.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 27.0}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "10-05-2024", "toDate": "10-05-2024", "fromTime": "09:00:00",
                                "toTime": "18:00:00"},
                      "region": {"id": 10747, "name": "\u041f\u043e\u0434\u043e\u043b\u044c\u0441\u043a",
                                 "type": "CITY", "parent": {"id": 98603,
                                                            "name": "\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u041f\u043e\u0434\u043e\u043b\u044c\u0441\u043a",
                                                            "type": "REPUBLIC_AREA", "parent": {"id": 1,
                                                                                                "name": "\u041c\u043e\u0441\u043a\u0432\u0430 \u0438 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                                "type": "REPUBLIC",
                                                                                                "parent": {"id": 3,
                                                                                                           "name": "\u0426\u0435\u043d\u0442\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                           "type": "COUNTRY_DISTRICT",
                                                                                                           "parent": {
                                                                                                               "id": 225,
                                                                                                               "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                               "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "142118",
                                  "city": "\u041f\u043e\u0434\u043e\u043b\u044c\u0441\u043a",
                                  "street": "\u042e\u0431\u0438\u043b\u0435\u0439\u043d\u0430\u044f \u0443\u043b\u0438\u0446\u0430",
                                  "gps": {"latitude": 55.418823, "longitude": 37.501736}}, "deliveryServiceId": 1005561,
                      "liftPrice": 0.0, "outletCode": "864", "shipments": [
                 {"id": 446292925, "shipmentDate": "08-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567438612, "fulfilmentId": "451603539-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": False},
        {"id": 451590078, "status": "PROCESSING", "substatus": "STARTED", "creationDate": "02-05-2024 09:34:18",
         "currency": "RUR", "itemsTotal": 3505.0, "deliveryTotal": 0.0, "buyerItemsTotal": 3505.0, "buyerTotal": 3505.0,
         "buyerItemsTotalBeforeDiscount": 3651.0, "buyerTotalBeforeDiscount": 3651.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591872888, "offerId": "ROSSVIK1282PRO",
                                                              "offerName": "ROSSVIK 1282PRO 12-8-2 PRO_\u0448\u0438\u043f \u0440\u0435\u043c\u043e\u043d\u0442\u043d\u044b\u0439! 12-8-2 \u0441\u0435\u0440\u0438\u044f pro (\u043a\u043e\u0440\u043e\u0431\u043a\u0430 500\u0448\u0442)\\",
                                                              "price": 3505.0, "buyerPrice": 3505.0,
                                                              "buyerPriceBeforeDiscount": 3651.0,
                                                              "priceBeforeDiscount": 3651.0, "count": 1,
                                                              "vat": "NO_VAT", "shopSku": "ROSSVIK1282PRO",
                                                              "subsidy": 146.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                                                              "subsidies": [{"type": "SUBSIDY", "amount": 146.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 146.0}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "12-05-2024", "toDate": "12-05-2024", "fromTime": "09:00:00",
                                "toTime": "18:00:00"}, "region": {"id": 54,
                                                                  "name": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                                                  "type": "CITY", "parent": {"id": 121110,
                                                                                             "name": "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u043e\u0435 \u043e\u0431\u0440\u0430\u0437\u043e\u0432\u0430\u043d\u0438\u0435 \u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                                                                             "type": "REPUBLIC_AREA",
                                                                                             "parent": {"id": 11162,
                                                                                                        "name": "\u0421\u0432\u0435\u0440\u0434\u043b\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                                        "type": "REPUBLIC",
                                                                                                        "parent": {
                                                                                                            "id": 52,
                                                                                                            "name": "\u0423\u0440\u0430\u043b\u044c\u0441\u043a\u0438\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                            "type": "COUNTRY_DISTRICT",
                                                                                                            "parent": {
                                                                                                                "id": 225,
                                                                                                                "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                                "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "620000",
                                  "city": "\u0415\u043a\u0430\u0442\u0435\u0440\u0438\u043d\u0431\u0443\u0440\u0433",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 \u0421\u043f\u0443\u0442\u043d\u0438\u043a\u043e\u0432",
                                  "apartment": "5", "gps": {"latitude": 56.758704, "longitude": 60.808187}},
                      "deliveryServiceId": 420399, "liftPrice": 0.0, "outletCode": "17614", "shipments": [
                 {"id": 446279464, "shipmentDate": "07-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567429039, "fulfilmentId": "451590078-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": False},
        {"id": 451559269, "status": "CANCELLED", "substatus": "CUSTOM", "creationDate": "02-05-2024 07:46:54",
         "currency": "RUR", "itemsTotal": 6294.0, "deliveryTotal": 0.0, "buyerItemsTotal": 6294.0, "buyerTotal": 6294.0,
         "buyerItemsTotalBeforeDiscount": 6358.0, "buyerTotalBeforeDiscount": 6358.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591838099, "offerId": "LUZARLRC0192B",
                                                              "offerName": "LUZAR LRC0192B \u0420\u0430\u0434\u0438\u0430\u0442\u043e\u0440 \u043e\u0445\u043b.\u0430\u043b\u044e\u043c.\u043d\u0435\u0441\u0431\u043e\u0440\u043d\u044b\u0439 \u0413\u0440\u0430\u043d\u0442\u0430 A/C LRc0192b",
                                                              "price": 6294.0, "buyerPrice": 6294.0,
                                                              "buyerPriceBeforeDiscount": 6358.0,
                                                              "priceBeforeDiscount": 6358.0, "count": 1,
                                                              "vat": "NO_VAT", "shopSku": "LUZARLRC0192B",
                                                              "subsidy": 64.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                                                              "subsidies": [{"type": "SUBSIDY", "amount": 64.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 64.0}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "11-05-2024", "toDate": "11-05-2024", "fromTime": "09:00:00",
                                "toTime": "18:00:00"},
                      "region": {"id": 195, "name": "\u0423\u043b\u044c\u044f\u043d\u043e\u0432\u0441\u043a",
                                 "type": "CITY", "parent": {"id": 120966,
                                                            "name": "\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0423\u043b\u044c\u044f\u043d\u043e\u0432\u0441\u043a",
                                                            "type": "REPUBLIC_AREA", "parent": {"id": 11153,
                                                                                                "name": "\u0423\u043b\u044c\u044f\u043d\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                                "type": "REPUBLIC",
                                                                                                "parent": {"id": 40,
                                                                                                           "name": "\u041f\u0440\u0438\u0432\u043e\u043b\u0436\u0441\u043a\u0438\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                           "type": "COUNTRY_DISTRICT",
                                                                                                           "parent": {
                                                                                                               "id": 225,
                                                                                                               "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                               "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "432030",
                                  "city": "\u0423\u043b\u044c\u044f\u043d\u043e\u0432\u0441\u043a",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 \u0422\u043e\u043b\u0431\u0443\u0445\u0438\u043d\u0430",
                                  "gps": {"latitude": 54.34214, "longitude": 48.364944}}, "deliveryServiceId": 686811,
                      "liftPrice": 0.0, "outletCode": "28532", "shipments": [
                 {"id": 446248658, "shipmentDate": "07-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567406975, "fulfilmentId": "451559269-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": True},
        {"id": 451549169, "status": "PROCESSING", "substatus": "STARTED", "creationDate": "02-05-2024 06:48:54",
         "currency": "RUR", "itemsTotal": 7020.0, "deliveryTotal": 0.0, "buyerItemsTotal": 7020.0, "buyerTotal": 7020.0,
         "buyerItemsTotalBeforeDiscount": 7020.0, "buyerTotalBeforeDiscount": 7020.0, "paymentType": "PREPAID",
         "paymentMethod": "YANDEX", "fake": False, "items": [{"id": 591826800, "offerId": "TREILER6012",
                                                              "offerName": "\u0422\u0440\u0435\u0439\u043b\u0435\u0440 6012 \u0424\u0430\u0440\u043a\u043e\u043f \u0442\u0440\u0435\u0439\u043b\u0435\u0440 Ford Focus II sedan 2004-2011",
                                                              "price": 7020.0, "buyerPrice": 7020.0,
                                                              "buyerPriceBeforeDiscount": 7020.0,
                                                              "priceBeforeDiscount": 7020.0, "count": 1,
                                                              "vat": "NO_VAT", "shopSku": "TREILER6012", "subsidy": 0.0,
                                                              "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0"}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "15-05-2024", "toDate": "15-05-2024", "fromTime": "10:00:00",
                                "toTime": "18:00:00"},
                      "region": {"id": 117646, "name": "\u0413\u0430\u043c\u043e\u0432\u043e", "type": "VILLAGE",
                                 "parent": {"id": 172872,
                                            "name": "\u0413\u0430\u043c\u043e\u0432\u0441\u043a\u043e\u0435 \u0441\u0435\u043b\u044c\u0441\u043a\u043e\u0435 \u043f\u043e\u0441\u0435\u043b\u0435\u043d\u0438\u0435",
                                            "type": "OTHER", "parent": {"id": 99658,
                                                                        "name": "\u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u0440\u0430\u0439\u043e\u043d",
                                                                        "type": "REPUBLIC_AREA", "parent": {"id": 11108,
                                                                                                            "name": "\u041f\u0435\u0440\u043c\u0441\u043a\u0438\u0439 \u043a\u0440\u0430\u0439",
                                                                                                            "type": "REPUBLIC",
                                                                                                            "parent": {
                                                                                                                "id": 40,
                                                                                                                "name": "\u041f\u0440\u0438\u0432\u043e\u043b\u0436\u0441\u043a\u0438\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                                "type": "COUNTRY_DISTRICT",
                                                                                                                "parent": {
                                                                                                                    "id": 225,
                                                                                                                    "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                                    "type": "COUNTRY"}}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "614512",
                                  "city": "\u0441\u0435\u043b\u043e \u0413\u0430\u043c\u043e\u0432\u043e",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 50 \u043b\u0435\u0442 \u041e\u043a\u0442\u044f\u0431\u0440\u044f",
                                  "gps": {"latitude": 57.870131, "longitude": 56.098541}}, "deliveryServiceId": 124261,
                      "liftPrice": 0.0, "outletCode": "7617", "shipments": [
                 {"id": 446238558, "shipmentDate": "08-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567401205, "fulfilmentId": "451549169-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": False},
        {"id": 451530744, "status": "CANCELLED", "substatus": "USER_REFUSED_DELIVERY",
         "creationDate": "02-05-2024 01:43:43", "currency": "RUR", "itemsTotal": 2934.0, "deliveryTotal": 0.0,
         "buyerItemsTotal": 2934.0, "buyerTotal": 2934.0, "buyerItemsTotalBeforeDiscount": 3280.0,
         "buyerTotalBeforeDiscount": 3280.0, "paymentType": "PREPAID", "paymentMethod": "YANDEX", "fake": False,
         "items": [{"id": 591805581, "offerId": "MILESDG2147201",
                    "offerName": "MILES DG21472-01 \u0410\u043c\u043e\u0440\u0442\u0438\u0437\u0430\u0442\u043e\u0440 \u043f\u0435\u0440\u0435\u0434\u043d\u0438\u0439 \u043f\u0440\u0430\u0432\u044b\u0439 OPEL CORSA D 06- (KYB 339714) DG21472-01",
                    "price": 2934.0, "buyerPrice": 2934.0, "buyerPriceBeforeDiscount": 3280.0,
                    "priceBeforeDiscount": 3280.0, "count": 1, "vat": "NO_VAT", "shopSku": "MILESDG2147201",
                    "subsidy": 346.0, "partnerWarehouseId": "0f2b9b09-b610-438a-9a97-d8f70d652df0",
                    "subsidies": [{"type": "SUBSIDY", "amount": 346.0}]}],
         "subsidies": [{"type": "SUBSIDY", "amount": 346.0}],
         "delivery": {"type": "PICKUP", "serviceName": "\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437",
                      "price": 0.0, "deliveryPartnerType": "YANDEX_MARKET",
                      "dates": {"fromDate": "11-05-2024", "toDate": "11-05-2024", "fromTime": "09:00:00",
                                "toTime": "18:00:00"},
                      "region": {"id": 11053, "name": "\u0428\u0430\u0445\u0442\u044b", "type": "CITY",
                                 "parent": {"id": 121151,
                                            "name": "\u0413\u043e\u0440\u043e\u0434\u0441\u043a\u043e\u0439 \u043e\u043a\u0440\u0443\u0433 \u0428\u0430\u0445\u0442\u044b",
                                            "type": "REPUBLIC_AREA", "parent": {"id": 11029,
                                                                                "name": "\u0420\u043e\u0441\u0442\u043e\u0432\u0441\u043a\u0430\u044f \u043e\u0431\u043b\u0430\u0441\u0442\u044c",
                                                                                "type": "REPUBLIC", "parent": {"id": 26,
                                                                                                               "name": "\u042e\u0436\u043d\u044b\u0439 \u0444\u0435\u0434\u0435\u0440\u0430\u043b\u044c\u043d\u044b\u0439 \u043e\u043a\u0440\u0443\u0433",
                                                                                                               "type": "COUNTRY_DISTRICT",
                                                                                                               "parent": {
                                                                                                                   "id": 225,
                                                                                                                   "name": "\u0420\u043e\u0441\u0441\u0438\u044f",
                                                                                                                   "type": "COUNTRY"}}}}},
                      "address": {"country": "\u0420\u043e\u0441\u0441\u0438\u044f", "postcode": "346503",
                                  "city": "\u0428\u0430\u0445\u0442\u044b",
                                  "street": "\u0443\u043b\u0438\u0446\u0430 \u0418\u043e\u043d\u043e\u0432\u0430",
                                  "gps": {"latitude": 47.724897, "longitude": 40.209932}}, "deliveryServiceId": 606235,
                      "liftPrice": 0.0, "outletCode": "25919", "shipments": [
                 {"id": 446220133, "shipmentDate": "07-05-2024", "shipmentTime": "11:30",
                  "boxes": [{"id": 567390693, "fulfilmentId": "451530744-1"}]}]}, "buyer": {"type": "PERSON"},
         "taxSystem": "USN", "cancelRequested": True}]}

ps_create_basket_answer = {
    "result": "ok",
    "data": {
        "id": 9288,
        "oem": "4214-0459-SX",
        "make_name": "STELLOX",
        "detail_name": "амортизатор передний газовый!\\ BMW E39 2.0-3.0/2.5TD/3.0D 95\u003e",
        "cost": 3762.0,
        "qnt": 2,
        "min_delivery_day": 1,
        "max_delivery_day": 3,
        "comment": "451642783"}}

FINAL_result = {"result": "ok", "data": [{"id": 76395, "oem": "42140459SX", "make_name": "STELLOX",
                                          "detail_name": "амортизатор передний газовый!\\ BMW E39 2.0-3.0/2.5TD/3.0D 95\u003e",
                                          "cost": 3762.0, "qnt": 2, "qnt_confirmed": 0, "qnt_accept": None,
                                          "qnt_income": None, "status": "Ожидает оплаты", "status_code": "processing",
                                          "comment": "451642783", "created_at": "2024-05-02T16:37:34.832+03:00",
                                          "order_id": 62821, "status_logs": [
        {"status_code": "processing", "status_name": "Ожидает оплаты",
         "created_at": "2024-05-02T16:37:35.074+03:00"}]}]}


# print(len(one) + len(two), len(tree))

# import re
#
# string = '3 товара за 200.00'
# pat = r'\d+.\d'
# match = re.search(pat, string)
# print(match.group())

def ran_input(n, m):
    line, num = '', 0
    length = len(str(m))
    for char in range(1, n + 1):
        line += str(char)
        num += char

    print(line, length, num, char)


# ran_input(15, 15)

yandex_order = {'id': 459557016, 'status': 'PROCESSING', 'substatus': 'STARTED', 'creationDate': '17-05-2024 13:53:35',
                'currency': 'RUR', 'itemsTotal': 6128.0, 'deliveryTotal': 0.0, 'buyerItemsTotal': 6128.0,
                'buyerTotal': 6128.0, 'buyerItemsTotalBeforeDiscount': 7382.0, 'buyerTotalBeforeDiscount': 7382.0,
                'paymentType': 'PREPAID', 'paymentMethod': 'YANDEX', 'fake': False,
                'items': [
                    {'id': 600992416, 'offerId': 'MILESDG11078',
                     'offerName': 'MILES DG11078 Амортизатор передний левый (OPEL ASTRA H/ZAFIRA 04-) (KYB 339703) DG11078',
                     'price': 3064.0, 'buyerPrice': 3064.0, 'buyerPriceBeforeDiscount': 3691.0,
                     'priceBeforeDiscount': 3691.0,
                     'count': 1, 'vat': 'NO_VAT', 'shopSku': 'MILESDG11078', 'subsidy': 627.0,
                     'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0',
                     'subsidies': [{'type': 'SUBSIDY', 'amount': 627.0}]},
                    {'id': 600992417,
                     'offerId': 'MILESDG21078',
                     'offerName': 'MILES DG21078 Амортизатор передний правый (OPEL ASTRA H/ZAFIRA 04-) (KYB 339702) DG21078',
                     'price': 3064.0, 'buyerPrice': 3064.0,
                     'buyerPriceBeforeDiscount': 3691.0,
                     'priceBeforeDiscount': 3691.0, 'count': 1,
                     'vat': 'NO_VAT', 'shopSku': 'MILESDG21078',
                     'subsidy': 627.0,
                     'partnerWarehouseId': '0f2b9b09-b610-438a-9a97-d8f70d652df0',
                     'subsidies': [{'type': 'SUBSIDY', 'amount': 627.0}]}],
                'subsidies': [{'type': 'SUBSIDY', 'amount': 1254.0}],
                'delivery': {'type': 'PICKUP', 'serviceName': 'Самовывоз', 'price': 0.0,
                             'deliveryPartnerType': 'YANDEX_MARKET',
                             'dates': {'fromDate': '29-05-2024', 'toDate': '29-05-2024', 'fromTime': '09:00:00',
                                       'toTime': '18:00:00'},
                             'region': {'id': 54, 'name': 'Екатеринбург', 'type': 'CITY',
                                        'parent': {'id': 121110, 'name': 'Муниципальное образование Екатеринбург',
                                                   'type': 'REPUBLIC_AREA',
                                                   'parent': {'id': 11162, 'name': 'Свердловская область',
                                                              'type': 'REPUBLIC', 'parent': {'id': 52,
                                                                                             'name': 'Уральский федеральный округ',
                                                                                             'type': 'COUNTRY_DISTRICT',
                                                                                             'parent': {'id': 225,
                                                                                                        'name': 'Россия',
                                                                                                        'type': 'COUNTRY'}}}}},
                             'address': {'country': 'Россия', 'postcode': '620105', 'city': 'Екатеринбург',
                                         'street': 'улица Рябинина',
                                         'gps': {'latitude': 56.786582, 'longitude': 60.496378}},
                             'deliveryServiceId': 522767, 'liftPrice': 0.0, 'outletCode': '20368', 'shipments': [
                        {'id': 454246228, 'shipmentDate': '24-05-2024', 'shipmentTime': '11:30',
                         'boxes': [{'id': 571559010, 'fulfilmentId': '459557016-1'}]}]}, 'buyer': {'type': 'PERSON'},
                'taxSystem': 'USN', 'cancelRequested': False}

from cred import ps_YM_II_api_key


def get_test(oem, brand):
    print(3333, oem, brand)
    # sys.exit()
    params = {
        "api_key": ps_YM_II_api_key,
        "oem": oem,
        "make_name": brand,
        "without_cross": True
    }
    metod = "/backend/price_items/api/v1/search/get_offers_by_oem_and_make_name"
    url = "http://3431.ru" + metod
    answer = requests.get(url, params=params)
    print(111111111111111111111, answer.text)
    print(2222222222222, answer.url)


response_ps_get_orders = {
    "status": "OK",
    "orders": [
        {
            "id": 70489,
            "order_id": 70489,
            "customer_id": 2063,
            "order_person": {
                "family_name": None,
                "second_name": None,
                "name": None
            },
            "auto_id": None,
            "id_1c": "site-70489-Yandeks Market II (2063)",
            "comment": "",
            "check_vin": False,
            "source_type": "api",
            "wait_assembling": False,
            "external_crm_id": None,
            "disable_balance_recalc": False,
            "customer": {
                "id": 2063,
                "user_id": 18,
                "region_id": 1,
                "ur_type": 0,
                "discount_type_id": 29,
                "is_supplier": False,
                "email": "auto_3431@ya.ru",
                "email_org": "", "pay_delay": 5,
                "credit_limit": 10000000.0,
                "name": "", "second_name": "",
                "family_name": "", "nds": 0.0,
                "send_email": True,
                "send_sms": False,
                "compile_name": "Яндекс Маркет II",
                "login_or_email": "auto_3431@ya.ru",
                "b1c_id": "",
                "customer_group_id": None,
                "client_type_id": None,
                "visible_zone_id": None,
                "tags": [],
                "delivery_route_id": None,
                "created_at": "2024-04-27T10:11:42.641+03:00",
                "essential": {
                    "company_name": "Яндекс Маркет II",
                    "company_type": "", "with_nds": False,
                    "inn": "", "kpp": "", "bik": "", "bank": "",
                    "city": None, "loro_account": "", "korr_schet": ""
                },
                "contact": {
                    "phone": "auto_3431", "cell_phone": ""
                },
                "delivery_address": {
                    "zip_code": "", "country": "",
                    "region": "", "city": "", "street": "",
                    "house": "", "korpus": "", "flat": ""
                },
                "official_address": {
                    "zip_code": "", "country": "", "region": "", "city": "",
                    "street": "", "house": "", "korpus": "", "flat": ""
                }
            },
            "delivery_address": {
                "zip_code": None, "country": None, "region": None, "city": None,
                "street": None, "house": None, "korpus": None, "flat": None,
                "passport": {
                    "number": None, "series": None, "issued": None, "issued_date": None,
                    "subdivision_code": None
                }
            },
            "essential": {
                "company_name": None, "company_type": None,
                "with_nds": False, "inn": None, "kpp": None, "bik": None,
                "bank": None, "city": None, "loro_account": None, "korr_schet": None
            },
            "delivery_type": "Доставка", "roistat_visit": None,
            "order_items": [
                {
                    "id": 85848, "region_order_item_id": None,
                    "divided_order_item_id": None,
                    "supplier_order_item_id": None,
                    "order_id": 70489, "price_id": 43,
                    "oem": "8733016SX", "make_name": "STELLOX",
                    "detail_name": "87-33016-SX_фара! левая с указателем поворота\\ MAN 19.233-... (F2000) 94\u003e",
                    "min_delivery_day": 1, "max_delivery_day": 1,
                    "first_cost": 4253.4, "cost": 5870.0, "qnt": 1,
                    "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None,
                    "volume_weight": 0, "length": None, "width": None, "height": None, "gtd": None,
                    "country": None, "status_id": 13, "supplier_status_name": None,
                    "check_best_price_status_id": None,
                    "sys_info": {
                        "weight": 3.34, "version": 0, "sup_logo": "ARMTEK_EMAIL_SPb",
                        "stat_group": 94, "ws_raw_cost": 4253.4, "distribyutor": False,
                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15416526",
                        "price_item_id": 3069861927, "raw_make_name": "STELLOX", "requested_oem": "8733016SX",
                        "visible_sup_logo": "ARMTEK_EMAIL_SPb", "central_warehouse": False, "client_visible_cost": 5870,
                        "requested_make_name": "STELLOX", "hide_visible_sup_logo_www": True,
                        "client_visible_cost_currency": "", "visible_delivery_day": "3 часа",
                        "checkout_options": "none", "min_qnt": 1},
                    "comment": "462016950",
                    "company_comment": None, "can_reorder": True,
                    "add_in_ws": False, "id_1c": "C2063O70489I85848",
                    "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
                    "updated_at": "2024-05-22T13:54:22.089+03:00",
                    "created_at": "2024-05-22T13:53:58.746+03:00",
                    "stock_batches": []
                },
                {
                    "id": 85847, "region_order_item_id": None,
                    "divided_order_item_id": None, "supplier_order_item_id": None,
                    "order_id": 70489, "price_id": 43, "oem": "8733017SX",
                    "make_name": "STELLOX",
                    "detail_name": "87-33017-SX_фара! правая с указателем. поворота\\ MAN 19.233-... (F2000) 94--\u003e",
                    "min_delivery_day": 1, "max_delivery_day": 1,
                    "first_cost": 3961.8,
                    "cost": 5467.0, "qnt": 1, "qnt_confirmed": 0,
                    "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
                    "length": None, "width": None, "height": None, "gtd": None, "country": None,
                    "status_id": 13, "supplier_status_name": None, "check_best_price_status_id": None,
                    "sys_info": {
                        "weight": 2.55, "version": 0,
                        "sup_logo": "ARMTEK_EMAIL_SPb", "stat_group": 94,
                        "ws_raw_cost": 3961.8, "distribyutor": False,
                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15416527",
                        "price_item_id": 3069861928, "raw_make_name": "STELLOX",
                        "requested_oem": "8733017SX", "visible_sup_logo": "ARMTEK_EMAIL_SPb",
                        "central_warehouse": False, "client_visible_cost": 5467,
                        "requested_make_name": "STELLOX", "hide_visible_sup_logo_www": True,
                        "client_visible_cost_currency": "", "visible_delivery_day": "3 часа",
                        "checkout_options": "none", "min_qnt": 1
                    },
                    "comment": "462016950",
                    "company_comment": None,
                    "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70489I85847",
                    "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
                    "updated_at": "2024-05-22T13:54:21.783+03:00", "created_at": "2024-05-22T13:53:58.735+03:00",
                    "stock_batches": []}],
            "marketplace_data": {},
            "marketplace_id": None,
            "load_order_client_number": None,
            "order_email_subject": None,
            "created_at": "2024-05-22T13:53:58.755+03:00",
            "updated_at": "2024-05-22T13:53:59.519+03:00"
        },
        {"id": 70488, "order_id": 70488, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70488-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85844, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70488, "price_id": 40, "oem": "LRC0563", "make_name": "LUZAR",
             "detail_name": "Радиатор охл. для а/м Chevrolet Lanos (97-) 1.5/1.6 MT (сборный) (LRc 0563)",
             "min_delivery_day": 2, "max_delivery_day": 3, "first_cost": 3765.91, "cost": 5197.0, "qnt": 1,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 5.087, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 3765.91, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14588129",
                          "inner_article": "7191", "price_item_id": 3069704123, "requested_oem": "LRC0563",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 5197, "requested_make_name": "LUZAR",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462029872", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70488I85844", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:53:20.213+03:00",
             "created_at": "2024-05-22T13:53:13.913+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:53:13.925+03:00", "updated_at": "2024-05-22T13:53:14.453+03:00"},
        {"id": 70487, "order_id": 70487, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70487-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85843, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70487, "price_id": 43, "oem": "5701135ASX", "make_name": "STELLOX",
             "detail_name": "57-01135A-SX_к-кт рычагов!\\ Audi A6 №Ch4B2031501\u003e, Skoda SuperB, VW Passat all 00\u003e",
             "min_delivery_day": 1, "max_delivery_day": 1, "first_cost": 11717.99, "cost": 15819.0, "qnt": 1,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 12, "version": 0, "sup_logo": "ARMTEK_EMAIL_SPb", "stat_group": 94,
                          "ws_raw_cost": 11717.99, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15403409",
                          "price_item_id": 3069800697, "raw_make_name": "STELLOX", "requested_oem": "5701135ASX",
                          "visible_sup_logo": "ARMTEK_EMAIL_SPb", "central_warehouse": False,
                          "client_visible_cost": 15819, "requested_make_name": "STELLOX",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "visible_delivery_day": "3 часа", "checkout_options": "none", "min_qnt": 1},
             "comment": "462039244", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70487I85843", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:53:14.390+03:00", "created_at": "2024-05-22T13:52:43.434+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:52:43.443+03:00",
         "updated_at": "2024-05-22T13:52:43.944+03:00"}, {"id": 70485, "order_id": 70485, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70485-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85841, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70485, "price_id": 91,
                                                                           "oem": "4300048R", "make_name": "METACO",
                                                                           "detail_name": "Рычаг передний правый",
                                                                           "min_delivery_day": 1, "max_delivery_day": 2,
                                                                           "first_cost": 2148.0, "cost": 2964.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 3.35, "version": 0,
                                                                                        "sup_logo": "Amtel-Euroauto",
                                                                                        "stat_group": 0,
                                                                                        "ws_raw_cost": 2148.0,
                                                                                        "distribyutor": False,
                                                                                        "applicability": "AUDI 100 91-94 / A6 94-97",
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/9274580",
                                                                                        "price_item_id": 3065300560,
                                                                                        "requested_oem": "4300048R",
                                                                                        "visible_sup_logo": "Amtel-Euroauto",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 2964,
                                                                                        "requested_make_name": "METACO",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462072864",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70485I85841",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:52:37.812+03:00",
                                                                           "created_at": "2024-05-22T13:52:19.868+03:00",
                                                                           "stock_batches": []},
                                                                          {"id": 85840, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70485, "price_id": 91,
                                                                           "oem": "4300048L", "make_name": "METACO",
                                                                           "detail_name": "Рычаг передний левый",
                                                                           "min_delivery_day": 1, "max_delivery_day": 2,
                                                                           "first_cost": 2242.0, "cost": 3094.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 3.568, "version": 0,
                                                                                        "sup_logo": "Amtel-Euroauto",
                                                                                        "stat_group": 0,
                                                                                        "ws_raw_cost": 2242.0,
                                                                                        "distribyutor": False,
                                                                                        "applicability": "AUDI 100 / A6  91-97",
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/9274578",
                                                                                        "price_item_id": 3065300563,
                                                                                        "requested_oem": "4300048L",
                                                                                        "visible_sup_logo": "Amtel-Euroauto",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 3094,
                                                                                        "requested_make_name": "METACO",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462072864",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70485I85840",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:52:37.516+03:00",
                                                                           "created_at": "2024-05-22T13:52:19.856+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:52:19.878+03:00",
                                                          "updated_at": "2024-05-22T13:52:20.619+03:00"},
        {"id": 70483, "order_id": 70483, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70483-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85837, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70483, "price_id": 43, "oem": "8400112SX", "make_name": "STELLOX",
             "detail_name": "84-00112-SX_пневмоподушка в сборе !2B-220-3 В:2отв.M10 1отв-шт.M12 Н:2отв. М10 216x215\\Scania, SAF",
             "min_delivery_day": 1, "max_delivery_day": 1, "first_cost": 2101.5, "cost": 2900.0, "qnt": 1,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 2.896, "version": 0, "sup_logo": "ARMTEK_EMAIL_SPb", "stat_group": 94,
                          "ws_raw_cost": 2101.5, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15412364",
                          "price_item_id": 3069858055, "raw_make_name": "STELLOX", "requested_oem": "8400112SX",
                          "visible_sup_logo": "ARMTEK_EMAIL_SPb", "central_warehouse": False,
                          "client_visible_cost": 2900, "requested_make_name": "STELLOX",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "visible_delivery_day": "3 часа", "checkout_options": "none", "min_qnt": 1},
             "comment": "462088171", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70483I85837", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:51:35.184+03:00", "created_at": "2024-05-22T13:51:21.922+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:51:21.931+03:00",
         "updated_at": "2024-05-22T13:51:22.511+03:00"}, {"id": 70482, "order_id": 70482, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70482-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85836, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70482, "price_id": 40,
                                                                           "oem": "M8011482", "make_name": "MARSHALL",
                                                                           "detail_name": "Амортизатор газ. передн. прав. Chery Tiggo 7 Pro 20-",
                                                                           "min_delivery_day": 2, "max_delivery_day": 3,
                                                                           "first_cost": 4742.0, "cost": 6544.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 5.54, "version": 0,
                                                                                        "sup_logo": "ПартКомСПб емайл",
                                                                                        "stat_group": 99,
                                                                                        "ws_raw_cost": 4742.0,
                                                                                        "distribyutor": False,
                                                                                        "goods_img_url": "",
                                                                                        "inner_article": "14089",
                                                                                        "price_item_id": 3069754612,
                                                                                        "requested_oem": "M8011482",
                                                                                        "visible_sup_logo": "ПартКомСПб емайл",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 6544,
                                                                                        "requested_make_name": "MARSHALL",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462092383",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70482I85836",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:51:14.665+03:00",
                                                                           "created_at": "2024-05-22T13:50:57.309+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:50:57.317+03:00",
                                                          "updated_at": "2024-05-22T13:50:57.903+03:00"},
        {"id": 70481, "order_id": 70481, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70481-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85833, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70481, "price_id": 6, "oem": "EX4841034050", "make_name": "MANDO",
             "detail_name": "Суппорт тормозной зад. Левый SSANGYONG ACTYON 10- EX4841034050", "min_delivery_day": 0,
             "max_delivery_day": 0, "first_cost": 5482.5, "cost": 7401.0, "qnt": 1, "qnt_confirmed": 0,
             "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None,
             "height": None, "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 3.086, "brand_id": "648", "sup_logo": "BERG SPB", "source_oem": "EX4841034050",
                          "stat_group": "100", "resource_id": "188772453", "ws_raw_cost": 5482.5, "distribyutor": False,
                          "warehouse_id": "16067213", "delivery_type": "1",
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/10721267",
                          "raw_make_name": "MANDO", "requested_oem": "EX4841034050", "ws_is_transit": False,
                          "visible_sup_logo": "BG0916", "central_warehouse": False, "client_visible_cost": 7401,
                          "requested_make_name": "MANDO", "source_min_delivery": "0", "return_without_problem": True,
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "return_without_problem_comment": "Заберем товар сами. Гарантия 30 дней. ",
                          "checkout_options": "none", "allowed_payment_type": "online", "min_qnt": 1},
             "comment": "462093775", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70481I85833", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:50:38.231+03:00", "created_at": "2024-05-22T13:50:27.372+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:50:27.389+03:00",
         "updated_at": "2024-05-22T13:50:28.028+03:00"}, {"id": 70479, "order_id": 70479, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70479-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85830, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70479, "price_id": 40,
                                                                           "oem": "VWB1701", "make_name": "STARTVOLT",
                                                                           "detail_name": "Моторедуктор стеклооч. задний для а/м Ssang Yong Kyron (05-) (VWB 1701)",
                                                                           "min_delivery_day": 2, "max_delivery_day": 3,
                                                                           "first_cost": 4562.43, "cost": 6296.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 1.1, "version": 0,
                                                                                        "sup_logo": "ПартКомСПб емайл",
                                                                                        "stat_group": 99,
                                                                                        "ws_raw_cost": 4562.43,
                                                                                        "distribyutor": False,
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14602289",
                                                                                        "inner_article": "7191",
                                                                                        "price_item_id": 3069702355,
                                                                                        "raw_make_name": "STARTVOLT",
                                                                                        "requested_oem": "VWB1701",
                                                                                        "visible_sup_logo": "ПартКомСПб емайл",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 6296,
                                                                                        "requested_make_name": "STARTVOLT",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462102870",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70479I85830",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:50:07.610+03:00",
                                                                           "created_at": "2024-05-22T13:49:53.971+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:49:53.979+03:00",
                                                          "updated_at": "2024-05-22T13:49:54.457+03:00"},
        {"id": 70478, "order_id": 70478, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70478-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85829, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70478, "price_id": 40, "oem": "EAM0103", "make_name": "TRIALLI",
             "detail_name": "Глушитель для а/м Лада 1118 Kalina доп. (резонатор) с гофрой (алюм. сталь) (EAM 0103)",
             "min_delivery_day": 2, "max_delivery_day": 3, "first_cost": 2211.54, "cost": 3052.0, "qnt": 1,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 6.2, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 2211.54, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14647447",
                          "inner_article": "7191", "price_item_id": 3069704262, "requested_oem": "EAM0103",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 3052, "requested_make_name": "TRIALLI",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462103348", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70478I85829", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:49:39.798+03:00",
             "created_at": "2024-05-22T13:49:32.519+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:49:32.531+03:00", "updated_at": "2024-05-22T13:49:33.049+03:00"},
        {"id": 70477, "order_id": 70477, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70477-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85828, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70477, "price_id": 40, "oem": "M8136531", "make_name": "MARSHALL",
             "detail_name": "Ступица передн. Volvo S60 II 10- / S80 II 06- / V60 I 10- / V70 III 07- / XC60 I 08- / XC70 II 07-",
             "min_delivery_day": 2, "max_delivery_day": 3, "first_cost": 4318.0, "cost": 5959.0, "qnt": 2,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 3.043, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 4318.0, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14929814",

"inner_article": "14089", "price_item_id": 3069756441, "requested_oem": "M8136531",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 5959, "requested_make_name": "MARSHALL",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462112373", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70477I85828", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:49:32.988+03:00",
             "created_at": "2024-05-22T13:49:08.445+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:49:08.455+03:00", "updated_at": "2024-05-22T13:49:08.954+03:00"},
        {"id": 70476, "order_id": 70476, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70476-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85827, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70476, "price_id": 40, "oem": "GO2404", "make_name": "TRIALLI",
             "detail_name": "ШРУС для а/м Suzuki SX4 (06-) (внутр. зад.) (GO 2404)", "min_delivery_day": 2,
             "max_delivery_day": 3, "first_cost": 4251.37, "cost": 5867.0, "qnt": 1, "qnt_confirmed": 0,
             "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None,
             "height": None, "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 1.57, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 4251.37, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14651685",
                          "inner_article": "7191", "price_item_id": 3069699777, "requested_oem": "GO2404",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 5867, "requested_make_name": "TRIALLI",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462138633", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70476I85827", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:48:48.701+03:00",
             "created_at": "2024-05-22T13:48:45.435+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:48:45.445+03:00", "updated_at": "2024-05-22T13:48:45.961+03:00"},
        {"id": 70475, "order_id": 70475, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70475-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85826, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70475, "price_id": 40, "oem": "KHB4263STD", "make_name": "KORTEX",
             "detail_name": "Ступица с подшипником CHEVROLET CAPTIVA/OPEL ANTARA 06- перед.(С ДАТЧИКОМ ABS)",
             "min_delivery_day": 2, "max_delivery_day": 3, "first_cost": 4017.93, "cost": 5545.0, "qnt": 2,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 4.79, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 4017.93, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/150832",
                          "inner_article": "15782", "price_item_id": 3069758969, "raw_make_name": "KORTEX",
                          "requested_oem": "KHB4263STD", "visible_sup_logo": "ПартКомСПб емайл",
                          "central_warehouse": False, "client_visible_cost": 5545, "requested_make_name": "KORTEX",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462160029", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70475I85826", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:48:45.887+03:00",
             "created_at": "2024-05-22T13:48:21.527+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:48:21.536+03:00", "updated_at": "2024-05-22T13:48:22.033+03:00"},
        {"id": 70474, "order_id": 70474, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70474-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85824, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70474, "price_id": 43, "oem": "6631107LLDEM", "make_name": "DEPO",
             "detail_name": "663-1107L-LD-EM_фара в сборе! левая с электрокорректором H1/H1/H7 \\ Iveco Daily 06-\u003e",
             "min_delivery_day": 1, "max_delivery_day": 1, "first_cost": 9637.73, "cost": 13011.0, "qnt": 1,
             "qnt_confirmed": 0, "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0,
             "length": None, "width": None, "height": None, "gtd": None, "country": None, "status_id": 13,
             "supplier_status_name": None, "check_best_price_status_id": None,
             "sys_info": {"weight": 8, "version": 0, "sup_logo": "ARMTEK_EMAIL_SPb", "stat_group": 94,
                          "ws_raw_cost": 9637.73, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/587606",
                          "price_item_id": 3069803549, "requested_oem": "6631107LLDEM",
                          "visible_sup_logo": "ARMTEK_EMAIL_SPb", "central_warehouse": False,
                          "client_visible_cost": 13011, "requested_make_name": "DEPO",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "visible_delivery_day": "3 часа", "checkout_options": "none", "min_qnt": 1},
             "comment": "462168370", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70474I85824", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:47:59.135+03:00", "created_at": "2024-05-22T13:47:56.716+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:47:56.726+03:00",
         "updated_at": "2024-05-22T13:47:57.282+03:00"}, {"id": 70473, "order_id": 70473, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70473-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85823, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70473, "price_id": 40,
                                                                           "oem": "GDB3424", "make_name": "TRW",
                                                                           "detail_name": "Колодки тормозные дисковые перед",
                                                                           "min_delivery_day": 2, "max_delivery_day": 3,
                                                                           "first_cost": 3712.0, "cost": 5123.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 1.633, "version": 0,
                                                                                        "sup_logo": "ПартКомСПб емайл",
                                                                                        "stat_group": 99,
                                                                                        "ws_raw_cost": 3712.0,
                                                                                        "distribyutor": False,
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/5608800",
                                                                                        "inner_article": "20",
                                                                                        "price_item_id": 3069667680,
                                                                                        "requested_oem": "GDB3424",
                                                                                        "visible_sup_logo": "ПартКомСПб емайл",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 5123,
                                                                                        "requested_make_name": "TRW",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462187662",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70473I85823",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:47:54.872+03:00",
                                                                           "created_at": "2024-05-22T13:47:27.191+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:47:27.199+03:00",
                                                          "updated_at": "2024-05-22T13:47:27.673+03:00"},
        {"id": 70472, "order_id": 70472, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70472-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85821, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70472, "price_id": 40, "oem": "OEM0372", "make_name": "OEM",
             "detail_name": "Бампер задний, Hyundai, Tucson, 1 JM (2004-2009)", "min_delivery_day": 2,
             "max_delivery_day": 3, "first_cost": 2542.8, "cost": 3509.0, "qnt": 1, "qnt_confirmed": 0,
             "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None,
             "height": None, "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 4.0455000000000005, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 2542.8, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15145515",
                          "inner_article": "13470", "price_item_id": 3069747957, "raw_make_name": "O.E.M.",
                          "requested_oem": "OEM0372", "visible_sup_logo": "ПартКомСПб емайл",
                          "central_warehouse": False, "client_visible_cost": 3509, "requested_make_name": "OEM",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462193583", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70472I85821", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:47:02.014+03:00",
             "created_at": "2024-05-22T13:46:50.590+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:46:50.601+03:00", "updated_at": "2024-05-22T13:46:51.161+03:00"},
        {"id": 70471, "order_id": 70471, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70471-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85820, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70471, "price_id": 43, "oem": "2717001", "make_name": "LEMFORDER",
             "detail_name": "2717001_сайлентблок задн.балки!\\ BMW X3 04\u003e", "min_delivery_day": 1,
             "max_delivery_day": 1, "first_cost": 2391.89, "cost": 3301.0, "qnt": 1, "qnt_confirmed": 0,
             "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None,
             "height": None, "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 0.318, "version": 0, "sup_logo": "ARMTEK_EMAIL_SPb", "stat_group": 94,
                          "ws_raw_cost": 2391.89, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/3905839",
                          "price_item_id": 3069788790, "raw_make_name": "LMI", "requested_oem": "2717001",
                          "visible_sup_logo": "ARMTEK_EMAIL_SPb", "central_warehouse": False,
                          "client_visible_cost": 3301, "requested_make_name": "LEMFORDER",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "visible_delivery_day": "3 часа", "checkout_options": "none", "min_qnt": 1},
             "comment": "462196896", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70471I85820", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:46:51.106+03:00", "created_at": "2024-05-22T13:46:26.471+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:46:26.480+03:00",
         "updated_at": "2024-05-22T13:46:27.020+03:00"}, {"id": 70469, "order_id": 70469, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70469-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85818, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70469, "price_id": 40,
                                                                           "oem": "DB62005", "make_name": "MILES",
                                                                           "detail_name": "Рычаг DAEWOO NEXIA/ESPERO/CHEVROLET LANOS пер.нижн. прав.",
                                                                           "min_delivery_day": 2, "max_delivery_day": 3,
                                                                           "first_cost": 2760.0, "cost": 3809.0,
                                                                           "qnt": 1, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 3.79, "version": 0,
                                                                                        "sup_logo": "ПартКомСПб емайл",
                                                                                        "stat_group": 99,
                                                                                        "ws_raw_cost": 2760.0,
                                                                                        "distribyutor": False,
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/12479017",
                                                                                        "inner_article": "20",
                                                                                        "price_item_id": 3069684689,
                                                                                        "raw_make_name": "MILES",
                                                                                        "requested_oem": "DB62005",
                                                                                        "visible_sup_logo": "ПартКомСПб емайл",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 3809,
                                                                                        "requested_make_name": "MILES",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462201344",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70469I85818",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:46:03.359+03:00",
                                                                           "created_at": "2024-05-22T13:45:56.013+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:45:56.026+03:00",
                                                          "updated_at": "2024-05-22T13:45:56.620+03:00"},
        {"id": 70468, "order_id": 70468, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70468-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85817, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70468, "price_id": 101, "oem": "LRAC0978", "make_name": "LUZAR",
             "detail_name": "Конденсер с ресивером Renault Logan II (12-) LRAC0978", "min_delivery_day": 0,
             "max_delivery_day": 1, "first_cost": 6365.3, "cost": 8593.0, "qnt": 1, "qnt_confirmed": 0,
             "qnt_accept": None, "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None,
             "height": None, "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 3.651, "version": 0, "sup_logo": "Berg-SPb-EMAIL", "stat_group": 97,
                          "ws_raw_cost": 6365.3, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/14587087",
                          "price_item_id": 3069956224, "requested_oem": "LRAC0978",
                          "visible_sup_logo": "Berg-SPb-EMAIL", "central_warehouse": False, "client_visible_cost": 8593,
                          "requested_make_name": "LUZAR", "hide_visible_sup_logo_www": True,
                          "client_visible_cost_currency": "", "checkout_options": "none", "min_qnt": 1},
             "comment": "462206705", "company_comment": None, "can_reorder": True, "add_in_ws": False,
             "id_1c": "C2063O70468I85817", "barcode": None, "cost_from_bonus": 0.0, "inwork_at": None,
             "updated_at": "2024-05-22T13:45:56.577+03:00", "created_at": "2024-05-22T13:45:28.436+03:00",
             "stock_batches": []}], "marketplace_data": {}, "marketplace_id": None, "load_order_client_number": None,
         "order_email_subject": None, "created_at": "2024-05-22T13:45:28.447+03:00",
         "updated_at": "2024-05-22T13:45:29.024+03:00"}, {"id": 70467, "order_id": 70467, "customer_id": 2063,
                                                          "order_person": {"family_name": None, "second_name": None,
                                                                           "name": None}, "auto_id": None,
                                                          "id_1c": "site-70467-Yandeks Market II (2063)", "comment": "",
                                                          "check_vin": False, "source_type": "api",
                                                          "wait_assembling": False, "external_crm_id": None,
                                                          "disable_balance_recalc": False,
                                                          "customer": {"id": 2063, "user_id": 18, "region_id": 1,
                                                                       "ur_type": 0, "discount_type_id": 29,
                                                                       "is_supplier": False, "email": "auto_3431@ya.ru",
                                                                       "email_org": "", "pay_delay": 5,
                                                                       "credit_limit": 10000000.0, "name": "",
                                                                       "second_name": "", "family_name": "", "nds": 0.0,
                                                                       "send_email": True, "send_sms": False,
                                                                       "compile_name": "Яндекс Маркет II",
                                                                       "login_or_email": "auto_3431@ya.ru",
                                                                       "b1c_id": "", "customer_group_id": None,
                                                                       "client_type_id": None, "visible_zone_id": None,
                                                                       "tags": [], "delivery_route_id": None,
                                                                       "created_at": "2024-04-27T10:11:42.641+03:00",
                                                                       "essential": {"company_name": "Яндекс Маркет II",
                                                                                     "company_type": "",
                                                                                     "with_nds": False, "inn": "",
                                                                                     "kpp": "", "bik": "", "bank": "",
                                                                                     "city": None, "loro_account": "",
                                                                                     "korr_schet": ""},
                                                                       "contact": {"phone": "auto_3431",
                                                                                   "cell_phone": ""},
                                                                       "delivery_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""},
                                                                       "official_address": {"zip_code": "",
                                                                                            "country": "", "region": "",
                                                                                            "city": "", "street": "",
                                                                                            "house": "", "korpus": "",
                                                                                            "flat": ""}},
                                                          "delivery_address": {"zip_code": None, "country": None,
                                                                               "region": None, "city": None,
                                                                               "street": None, "house": None,
                                                                               "korpus": None, "flat": None,
                                                                               "passport": {"number": None,
                                                                                            "series": None,
                                                                                            "issued": None,
                                                                                            "issued_date": None,
                                                                                            "subdivision_code": None}},
                                                          "essential": {"company_name": None, "company_type": None,
                                                                        "with_nds": False, "inn": None, "kpp": None,
                                                                        "bik": None, "bank": None, "city": None,
                                                                        "loro_account": None, "korr_schet": None},
                                                          "delivery_type": "Доставка", "roistat_visit": None,
                                                          "order_items": [{"id": 85815, "region_order_item_id": None,
                                                                           "divided_order_item_id": None,
                                                                           "supplier_order_item_id": None,
                                                                           "order_id": 70467, "price_id": 43,
                                                                           "oem": "8717608SX", "make_name": "STELLOX",
                                                                           "detail_name": "87-17608-SX_крыло полуприцепа! с креплением, 450х700, с брызговиком антиспрей L=350мм\\ Universal",
                                                                           "min_delivery_day": 1, "max_delivery_day": 1,
                                                                           "first_cost": 3100.49, "cost": 4279.0,
                                                                           "qnt": 2, "qnt_confirmed": 0,
                                                                           "qnt_accept": None, "qnt_income": None,
                                                                           "weight": None, "volume_weight": 0,
                                                                           "length": None, "width": None,
                                                                           "height": None, "gtd": None, "country": None,
                                                                           "status_id": 13,
                                                                           "supplier_status_name": None,
                                                                           "check_best_price_status_id": None,
                                                                           "sys_info": {"weight": 2.3, "version": 0,
                                                                                        "sup_logo": "ARMTEK_EMAIL_SPb",
                                                                                        "stat_group": 94,
                                                                                        "ws_raw_cost": 3100.49,
                                                                                        "distribyutor": False,
                                                                                        "goods_img_url": "https://img-server-10.parts-soft.ru/images/1554/15415895",
                                                                                        "price_item_id": 3069861452,
                                                                                        "raw_make_name": "STELLOX",
                                                                                        "requested_oem": "8717608SX",
                                                                                        "visible_sup_logo": "ARMTEK_EMAIL_SPb",
                                                                                        "central_warehouse": False,
                                                                                        "client_visible_cost": 4279,
                                                                                        "requested_make_name": "STELLOX",
                                                                                        "hide_visible_sup_logo_www": True,
                                                                                        "client_visible_cost_currency": "",
                                                                                        "visible_delivery_day": "3 часа",
                                                                                        "checkout_options": "none",
                                                                                        "min_qnt": 1},
                                                                           "comment": "462211255",
                                                                           "company_comment": None, "can_reorder": True,
                                                                           "add_in_ws": False,
                                                                           "id_1c": "C2063O70467I85815",
                                                                           "barcode": None, "cost_from_bonus": 0.0,
                                                                           "inwork_at": None,
                                                                           "updated_at": "2024-05-22T13:45:04.173+03:00",
                                                                           "created_at": "2024-05-22T13:45:00.253+03:00",
                                                                           "stock_batches": []}],
                                                          "marketplace_data": {}, "marketplace_id": None,
                                                          "load_order_client_number": None, "order_email_subject": None,
                                                          "created_at": "2024-05-22T13:45:00.265+03:00",
                                                          "updated_at": "2024-05-22T13:45:00.711+03:00"},
        {"id": 70465, "order_id": 70465, "customer_id": 2063,
         "order_person": {"family_name": None, "second_name": None, "name": None}, "auto_id": None,
         "id_1c": "site-70465-Yandeks Market II (2063)", "comment": "", "check_vin": False, "source_type": "api",
         "wait_assembling": False, "external_crm_id": None, "disable_balance_recalc": False,
         "customer": {"id": 2063, "user_id": 18, "region_id": 1, "ur_type": 0, "discount_type_id": 29,
                      "is_supplier": False, "email": "auto_3431@ya.ru", "email_org": "", "pay_delay": 5,
                      "credit_limit": 10000000.0, "name": "", "second_name": "", "family_name": "", "nds": 0.0,
                      "send_email": True, "send_sms": False, "compile_name": "Яндекс Маркет II",
                      "login_or_email": "auto_3431@ya.ru", "b1c_id": "", "customer_group_id": None,
                      "client_type_id": None, "visible_zone_id": None, "tags": [], "delivery_route_id": None,
                      "created_at": "2024-04-27T10:11:42.641+03:00",
                      "essential": {"company_name": "Яндекс Маркет II", "company_type": "", "with_nds": False,
                                    "inn": "", "kpp": "", "bik": "", "bank": "", "city": None, "loro_account": "",
                                    "korr_schet": ""}, "contact": {"phone": "auto_3431", "cell_phone": ""},
                      "delivery_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""},
                      "official_address": {"zip_code": "", "country": "", "region": "", "city": "", "street": "",
                                           "house": "", "korpus": "", "flat": ""}},
         "delivery_address": {"zip_code": None, "country": None, "region": None, "city": None, "street": None,
                              "house": None, "korpus": None, "flat": None,
                              "passport": {"number": None, "series": None, "issued": None, "issued_date": None,
                                           "subdivision_code": None}},
         "essential": {"company_name": None, "company_type": None, "with_nds": False, "inn": None, "kpp": None,
                       "bik": None, "bank": None, "city": None, "loro_account": None, "korr_schet": None},
         "delivery_type": "Доставка", "roistat_visit": None, "order_items": [
            {"id": 85813, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70465, "price_id": 40, "oem": "AAB2905110", "make_name": "LIFAN",
             "detail_name": "Амортизатор передний левый", "min_delivery_day": 2, "max_delivery_day": 3,
             "first_cost": 2323.41, "cost": 3206.0, "qnt": 1, "qnt_confirmed": 0, "qnt_accept": None,
             "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None, "height": None,
             "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 4.329, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 2323.41, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/labels/1554/72/AAB2905110/1.svg?detail_name=%D0%90%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80+%D0%BF%D0%B5%D1%80+%D0%BB%D0%B5%D0%B2",
                          "inner_article": "20", "price_item_id": 3069689057, "requested_oem": "AAB2905110",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 3206, "requested_make_name": "LIFAN",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462212609", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70465I85813", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:44:49.605+03:00",
             "created_at": "2024-05-22T13:44:36.890+03:00", "stock_batches": []},
            {"id": 85812, "region_order_item_id": None, "divided_order_item_id": None, "supplier_order_item_id": None,
             "order_id": 70465, "price_id": 40, "oem": "AAB2905610", "make_name": "LIFAN",
             "detail_name": "Амортизатор передний правый", "min_delivery_day": 2, "max_delivery_day": 3,
             "first_cost": 2850.15, "cost": 3933.0, "qnt": 1, "qnt_confirmed": 0, "qnt_accept": None,
             "qnt_income": None, "weight": None, "volume_weight": 0, "length": None, "width": None, "height": None,
             "gtd": None, "country": None, "status_id": 13, "supplier_status_name": None,
             "check_best_price_status_id": None,
             "sys_info": {"weight": 4.36, "version": 0, "sup_logo": "ПартКомСПб емайл", "stat_group": 99,
                          "ws_raw_cost": 2850.15, "distribyutor": False,
                          "goods_img_url": "https://img-server-10.parts-soft.ru/labels/1554/72/AAB2905610/1.svg?detail_name=%D0%90%D0%BC%D0%BE%D1%80%D1%82%D0%B8%D0%B7%D0%B0%D1%82%D0%BE%D1%80+%D0%BF%D0%B5%D1%80+%D0%BF%D1%80%D0%B0%D0%B2",
                          "inner_article": "20", "price_item_id": 3069690948, "requested_oem": "AAB2905610",
                          "visible_sup_logo": "ПартКомСПб емайл", "central_warehouse": False,
                          "client_visible_cost": 3933, "requested_make_name": "LIFAN",
                          "hide_visible_sup_logo_www": True, "client_visible_cost_currency": "",
                          "checkout_options": "none", "min_qnt": 1}, "comment": "462212609", "company_comment": None,
             "can_reorder": True, "add_in_ws": False, "id_1c": "C2063O70465I85812", "barcode": None,
             "cost_from_bonus": 0.0, "inwork_at": None, "updated_at": "2024-05-22T13:44:49.317+03:00",
             "created_at": "2024-05-22T13:44:36.879+03:00", "stock_batches": []}], "marketplace_data": {},
         "marketplace_id": None, "load_order_client_number": None, "order_email_subject": None,
         "created_at": "2024-05-22T13:44:36.901+03:00", "updated_at": "2024-05-22T13:44:37.693+03:00"}]}

result_from_ps = {
    "result":"ok",
    "data":{
        "id":11176,
        "oem":"0701099SX",
        "make_name":"STELLOX",
        "detail_name":"07-01099-SX_к-кт сцепления!\\ Honda CR-V 2.0 95\u003e","cost":5993.0,
        "qnt":1,"min_delivery_day":1,"max_delivery_day":1,
        "comment":"463481305"
    }}

FINAL_result = {
    "result":"ok",
    "data":[
        {
            "id":87102,
            "oem":"0701099SX",
            "make_name":"STELLOX",
            "detail_name":"07-01099-SX_к-кт сцепления!\\ Honda CR-V 2.0 95\u003e",
            "cost":5993.0,"qnt":1,"qnt_confirmed":0,
            "qnt_accept":None,"qnt_income":None,
            "status":"Ожидает оплаты",
            "status_code":"processing",
            "comment":"463481305",
            "created_at":"2024-05-24T16:01:32.449+03:00",
            "order_id":71333,
            "status_logs":[
                {"status_code":"processing",
                 "status_name":"Ожидает оплаты",
                 "created_at":"2024-05-24T16:01:32.648+03:00"}]}]}

