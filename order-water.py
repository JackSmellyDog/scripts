import requests
import random
import datetime
import hashlib
import urllib.parse

BASE_URL = 'https://www.clearwater.ua/'
ORDER_PAGE_URL = BASE_URL + 'ua/order/'
ORDER_URL = BASE_URL + 'ajax/'

# vars that need to be updated
CLIENT_NAME='YOUR_CLIENT_NAME'
FROM_TIME = '09.00'
TO_TIME = '12.00'
CITY = 'YOUR_CITY'
STREET = 'YOUR_STREET'
HOUSE = 'YOUR_HOUSE',
OFFICE = 'YOUR_OFFICE',
ENTRANCE = 'YOUR_ENTRANCE',
FLOOR = 'YOUR_FLOOR',
COMMENT = '',
ORDER_NOTES = '',
CONTACT = 'YOUR_NAME',
CONTACT_PHONE = 'YOUR_PHONE_NUMBER',
CONF_SMS = 'YOUR_PHONE_NUMBER',
GOODS_CODE = '____29___',
GOODS_NUMBER = 3,

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}


def create_payload(body: dict) -> str:
    key_value_pair_array = []

    for k, v in body.items():
        encoded_key = urllib.parse.quote_plus(str(k).encode('utf-8'))
        encoded_value = urllib.parse.quote_plus(str(v).encode('utf-8'))

        key_value_pair_array.append(f'{encoded_key}={encoded_value}')

    return '&'.join(key_value_pair_array)


def create_md5_hash(payload: str):
    return hashlib.md5(payload.encode('utf-8')).hexdigest()


def tomorrow():
    return datetime.date.today() + datetime.timedelta(days=1)


def create_order_request_body(
    token,
    address_id,
    order_id,
    delivery_date,
    client_name=CLIENT_NAME,
    from_time=FROM_TIME,
    to_time=TO_TIME,
    city=CITY,
    street=STREET,
    house=HOUSE,
    office=OFFICE,
    entrance=ENTRANCE,
    floor=FLOOR,
    comment=COMMENT,
    order_notes=ORDER_NOTES,
    contact=CONTACT,
    contact_phone=CONTACT_PHONE,
    conf_sms=CONF_SMS,
    goods_code=GOODS_CODE,
    goods_number=GOODS_NUMBER,
) -> dict:
    return {
        'TOKEN': token,
        'orderForm[ClientName]': client_name,
        'orderForm[AddresID]': address_id,
        'orderForm[OrderID]': order_id,
        'orderForm[DeliveryDate]': delivery_date,
        'orderForm[From]': from_time,
        'orderForm[To]': to_time,
        'orderForm[City]': city,
        'orderForm[Street]': street,
        'orderForm[House]': house,
        'orderForm[Office]': office,
        'orderForm[Entrance]': entrance,
        'orderForm[Floor_]': floor,
        'orderForm[Comm]': comment,
        'orderForm[OrderNotes]': order_notes,
        'orderForm[Contact]': contact,
        'orderForm[ContPhone]': contact_phone,
        'orderForm[ConfSMS]': conf_sms,
        'orderForm[Goods][0][Name]': '0',
        'orderForm[Goods][0][Code]': goods_code,
        'orderForm[Goods][0][Num]': goods_number,
        'orderForm[Goods][0][Price]': '0'
    }


def send_request(body, cookies, hash, headers=HEADERS, url=ORDER_URL):
    r = requests.post(f'{url}?ft={hash}', data=body,
                      headers=headers, cookies=cookies)
    print(r.text)


def main(order_page_url=ORDER_PAGE_URL):
    res = requests.get(order_page_url)
    cookies = res.cookies.get_dict()

    order_request_body = create_order_request_body(
        token=cookies.get('CW_VAR'),
        address_id=create_md5_hash(str(random.random())[:18]),
        order_id=create_md5_hash(str(random.random())[:18]),
        delivery_date=tomorrow().strftime('%d.%m.%Y')
    )

    payload = create_payload(order_request_body)

    hash = create_md5_hash(payload)

    send_request(body=payload, cookies=cookies, hash=hash)


if __name__ == "__main__":
    main()
