proxy_sper = {
  "data": {
    "merchantId": 5046,
    "shipments": [
      {
        "shipmentId": "946032218",
        "shipmentDate": "2021-02-17T09:34:03+03:00",
        "items": [
          {
            "itemIndex": "1",
            "goodsId": "100023763738",
            "offerId": "3951",
            "itemName": "Вертикальный пылесос Kitfort  KT-535-2 White",
            "price": 11990,
            "finalPrice": 5995,
            "discounts": [
              {
                "discountType": "BPG20",
                "discountDescription": "BPG20",
                "discountAmount": 1424
              },
              {
                "discountType": "LOY",
                "discountDescription": "Скидка БР",
                "discountAmount": 4571
              }
            ],
            "quantity": 1,
            "taxRate": "20",
            "reservationPerformed": True,
            "isDigitalMarkRequired": False
          }
        ],
        "label": {
          "deliveryId": "933021193",
          "region": "Воронежская",
          "city": "Воронеж",
          "address": "Россия, Воронежская обл.,  Воронеж, Проспект Губкина, 9",
          "fullName": "Петров Пётр",
          "merchantName": "ООО \"АЭРО-ТРЕЙД\"",
          "merchantId": 5046,
          "shipmentId": "956032218",
          "shippingDate": "2021-02-21T17:00:00+03:00",
          "deliveryType": "Самовывоз из пункта выдачи",
          "labelText": "<!DOCTYPE html>\n<html>\n<head>\n    <meta charset=\"UTF-8\"/>\t\n    <title>Маркировочный лист</title>    ..."
        },
        "shipping": {
          "shippingDate": "2021-02-21T17:00:00+03:00",
          "shippingPoint": 132378
        },
        "fulfillmentMethod": "FULFILLMENT_BY_MERCHANT"
      }
    ]
  },
  "meta": {
    "source": "OMS"
  }
}

proxy_lm = {
   "id":"MP1703473-001",
   "pickup":{},
   "products":[
      {
         "lmId":"90115665",
         "vendorCode":"BT2834B",
         "price":5860,
         "qty":3,
         "comissionRate":0
      },
      {
         "lmId":"90121362",
         "vendorCode":"HPUV65ELC",
         "price":5860,
         "qty":3,
         "comissionRate":0
      }
   ],
   "deliveryCost":0,
   "parcelPrice":5860,
   "creationDate":"2022-12-14",
   "promisedDeliveryDate":"2022-12-22",
   "calculatedWeight":4.8,
   "calculatedLength":707,
   "calculatedHeight":156,
   "calculatedWidth":686
}

proxy_ym = {
  "order":
  {
    "businessId": 3675591,
    "currency": "RUR",
    "fake": False,
    "id": 12345,
    "paymentType": "PREPAID",
    "paymentMethod": "YANDEX",
    "taxSystem": "OSN",
    "subsidyTotal": 150,
    "buyerItemsTotalBeforeDiscount": 5800,
    "buyerTotalBeforeDiscount": 6150,
    "buyerItemsTotal": 5650,
    "buyerTotal": 6000,
    "itemsTotal": 5650,
    "total": 6000,
    "totalWithSubsidy": 6150,
    "deliveryTotal": 350,
    "delivery":
    {"shipments":
       [
        {
         "id": 90141,
         "weight": 350,
         "width": 10,
         "height": 20,
         "depth": 7,
         "status": "CREATED",
         "shipmentDate": "11-12-2021",
         "shipmentTime": "11:30"
        }
       ],
       "dates": { "fromDate": "11-12-2021", "toDate": "11-12-2021", "fromTime": "11:28", "toTime": "12:08" }, "serviceName": "СПСР",
      "type": "DELIVERY",
      "subsidy": 300,
      "region":
      {
        "id": 213,
        "name": "Москва",
        "type": "CITY",
        "parent":
        {
          "id": 1,
          "name": "Москва и Московская область",
          "type": "SUBJECT_FEDERATION",
          "parent":
          {
            "id": 3,
            "name": "Центральный федеральный округ",
            "type": "COUNTRY_DISTRICT",
            "parent":
            {
              "id": 225,
              "name": "Россия",
              "type": "COUNTRY"
            }
          }
        }
      }
    },
    "items":
    [
      {
        "id": 12345,
        "feedId": 56789,
        "offerId": "4609283881",
        "offerName": "Чайник электрический 100 W",
        "price": 1150,
        "buyer-price": 1150,
        "buyerPriceBeforeDiscount": 1200,
        "subsidy": 50,
        "count": 3,
        "delivery": True,
        "params": "Цвет товара: white",
        "vat": "VAT_20",
        "fulfilmentShopId": 325235,
        "sku": "150714598463",
        "shopSku": "4609283881", "warehouseId": 12345, "partnerWarehouseId": "67890"
      },
      {
        "id": 42349,
        "feedId": 9858375,
        "offerId": "4607632101",
        "offerName": "Тостер",
        "price": 2200,
        "buyer-price": 2200,
        "buyerPriceBeforeDiscount": 2200,
        "subsidy": 0,
        "count": 1,
        "delivery": True,
        "params": "Количество отделений: 2",
        "vat": "VAT_20",
        "fulfilmentShopId": 785393,
        "sku": "107573963056",
        "shopSku": "4607632101", "warehouseId": 12345, "partnerWarehouseId": "67890"
      }
    ]
  }
}

proxy_wb = {
   "supplies":[
      {
         "closedAt":"2023-03-02T06:06:52Z",
         "scanDt":"2023-03-02T10:46:19Z",
         "isLargeCargo":False,
         "id":"WB-GI-41066137",
         "name":"Поставка на 02.03",
         "createdAt":"2023-03-01T09:32:40Z",
         "done":True
      },
      {
         "closedAt":"None",
         "scanDt":"None",
         "isLargeCargo":False,
         "id":"WB-GI-41149707",
         "name":"Поставка на 03.03",
         "createdAt":"2023-03-02T08:42:16Z",
         "done":False
      }
   ],
   "next":32899717
}

proxy_wb_orders = {
   "orders":[
      {
         "user":"None",
         "orderUid":"20903194_19451597073848538",
         "article":"OWLB191044",
         "rid":"19451597073848538.0.0",
         "createdAt":"2023-03-02T07:24:36Z",
         "offices":[
            "Москва"
         ],
         "skus":[
            "6973720591070"
         ],
         "prioritySc":[

         ],
         "id":698387374,
         "warehouseId":664706,
         "nmId":143537174,
         "chrtId":242393399,
         "price":332800,
         "convertedPrice":332800,
         "currencyCode":643,
         "convertedCurrencyCode":643,
         "isLargeCargo":False
      },
      {
         "user":"None",
         "orderUid":"15174043_16587021573848740",
         "article":"OWLC19-014",
         "rid":"16587021573848740.0.0",
         "createdAt":"2023-03-02T07:31:19Z",
         "offices":[
            "Москва"
         ],
         "skus":[
            "6973772600966"
         ],
         "prioritySc":[

         ],
         "id":698399204,
         "warehouseId":664706,
         "nmId":145721888,
         "chrtId":245485480,
         "price":232900,
         "convertedPrice":232900,
         "currencyCode":643,
         "convertedCurrencyCode":643,
         "isLargeCargo":False
      },
      {
         "user":"None",
         "orderUid":"4591153_11295576573850246",
         "article":"OWLC19-007",
         "rid":"11295576573850246.0.0",
         "createdAt":"2023-03-02T08:21:34Z",
         "offices":[
            "Москва"
         ],
         "skus":[
            "6973720577487"
         ],
         "prioritySc":[
            "Коледино"
         ],
         "id":698491674,
         "warehouseId":664706,
         "nmId":145721887,
         "chrtId":245485479,
         "price":366100,
         "convertedPrice":366100,
         "currencyCode":643,
         "convertedCurrencyCode":643,
         "isLargeCargo":False
      },
      {
         "user":"None",
         "orderUid":"3082585_10541292573850611",
         "article":"OWLC19-014",
         "rid":"10541292573850611.0.0",
         "createdAt":"2023-03-02T08:33:43Z",
         "offices":[
            "Москва"
         ],
         "skus":[
            "6973772600966"
         ],
         "prioritySc":[

         ],
         "id":698514709,
         "warehouseId":664706,
         "nmId":145721888,
         "chrtId":245485480,
         "price":232900,
         "convertedPrice":232900,
         "currencyCode":643,
         "convertedCurrencyCode":643,
         "isLargeCargo":False
      }
   ]
}