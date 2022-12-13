import csv
import json

import requests
import pandas as pd

from cookies_and_headers import cookies, headers


def get_data(custom_status_id, month='October'):
    """ """
    with open(f'orders_list_{month}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'id',
                'order_type',
                'client_full_name',
                'payment_option_name',
                'quantity',
                'comments',
                'sku',
                'totalPriceRate'
            )
        )
    response = requests.get(
        f'https://my.prom.ua/remote/order_api/orders?custom_status_id={custom_status_id}&'
        f'company_client_id=null&page=1&per_page=100&new_cabinet=true&search_term',
        cookies=cookies,
        headers=headers,
    ).json()

    # with open('orders_list.json', 'w', encoding='utf-8') as file:
    #     json.dump(response, file, indent=4, ensure_ascii=False)

    pagination = response.get('pagination').get('num_pages')

    for page in range(1, pagination + 1):
        response = requests.get(
            f'https://my.prom.ua/remote/order_api/orders?custom_status_id=127894&company_client_id=null&page={page}&'
            f'per_page=100&new_cabinet=true&search_term',
            cookies=cookies,
            headers=headers,
        ).json()

        # with open(f'orders_list_{page}.json', 'w', encoding='utf-8') as file:
        #     json.dump(response, file, indent=4, ensure_ascii=False)

        orders = response.get('orders')

        for order in orders:
            id = order.get('id')
            order_type = order.get('type')
            client_first_name = order.get('client_first_name')
            client_last_name = order.get('client_last_name')
            client_full_name = client_last_name + ' ' + client_first_name
            payment_option_name = order.get('payment_option_name')
            labels = order.get('labels')
            comments = ', '.join([label.get('name').replace(' ', '') for label in labels])
            added_items = order.get('added_items')

            for item in added_items:
                sku = item.get('sku')
                quantity = item.get('quantity')
                totalPriceRate = item.get('totalPriceRate')

                with open(f'orders_list_{month}.csv', 'a', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            id,
                            order_type,
                            client_full_name,
                            payment_option_name,
                            quantity,
                            comments,
                            sku,
                            totalPriceRate
                        )
                    )

                read_file = pd.read_csv(f'orders_list_{month}.csv')

                read_file.to_excel(f'order_list_{month}.xlsx', index=None, header=True)


def main():
    get_data(custom_status_id=127894)


if __name__ == '__main__':
    main()