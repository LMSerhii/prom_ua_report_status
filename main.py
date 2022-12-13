import csv

import requests

from cookies_and_headers import cookies, headers


def get_data(custom_status_id, month=None):
    """ """

    response = requests.get(
        f'https://my.prom.ua/remote/order_api/orders?custom_status_id={custom_status_id}&company_client_id=null&page=1&'
        'per_page=100&new_cabinet=true&search_term',
        cookies=cookies,
        headers=headers,
    ).json()

    pagination = response.get('pagination').get('num_pages')

    for page in range(1, pagination + 1):
        response = requests.get(
            f'https://my.prom.ua/remote/order_api/orders?custom_status_id=127894&company_client_id=null&page={page}&'
            'per_page=100&new_cabinet=true&search_term',
            cookies=cookies,
            headers=headers,
        ).json()

    data = {}
    orders = response.get('orders')
    for order in orders:
        id = order.get('id')
        order_type = order.get('type')
        client_first_name = order.get('client_first_name')
        client_last_name = order.get('client_last_name')
        client_full_name = client_last_name + ' ' + client_first_name
        client_phone = order.get('client_phone')
        delivery_option_name = order.get('delivery_option_name')
        price_text = order.get('price_text')
        payment_option_name = order.get('payment_option_name')
        labels = order.get('labels')
        comments = ', '.join([label.get('name').replace(' ', '') for label in labels])
        added_items = order.get('added_items')

        #####
        for item in added_items:
            sku = item.get('sku')
            quantity = item.get('quantity')
            totalPriceRate = item.get('totalPriceRate')


def main():
    get_data(custom_status_id=127894, month='October')


if __name__ == '__main__':
    main()