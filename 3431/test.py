

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
            "silent": false
      }
}
