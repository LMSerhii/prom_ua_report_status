import csv
import requests
import pandas as pd

from tqdm import tqdm

from cookies_and_headers import cookies, headers
from get_status import read_excel


def get_data(custom_status_id, month='October'):
    """ Отправляем запросы на получение данных в формат json,
    через авторизированный кабинет для вытягивания интересующей информации.
    Первая часть - запрос на общий статус заказов,
    Вторая часть - запрос на почтовые данные
    """

    # создание файла с заголовками
    with open(f'data/orders_list_{month}.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'id',
                'order_type',
                'client_full_name',
                'payment_option_name',
                'quantity',
                'sku',
                'comments',
                'ttn',
                'price',
                'deliveryCost'
            )
        )

    # Отправляем get запрос для получения пагинации
    response = requests.get(
        f'https://my.prom.ua/remote/order_api/orders?custom_status_id={custom_status_id}&'
        f'company_client_id=null&page=1&per_page=100&new_cabinet=true&search_term',
        cookies=cookies,
        headers=headers,
    ).json()

    pagination = response.get('pagination').get('num_pages')

    # Проходим циклом по всем страницам получаем json с данными

    for page in tqdm(range(1, pagination + 1)):
        response = requests.get(
            f'https://my.prom.ua/remote/order_api/orders?custom_status_id={custom_status_id}&company_client_id=null&page={page}&'
            f'per_page=100&new_cabinet=true&search_term',
            cookies=cookies,
            headers=headers,
        ).json()

        # Забираем нужные данные
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

            # Отправляем новый запрос, что бы получить недостающие данные

            params = {
                'order_id': f'{id}',
                'delivery_option_id': '4898969',
                'is_np_pochtomat': 'true',
                'cart_total_price': '692.8',
            }

            response = requests.get(
                'https://my.prom.ua/remote/delivery/nova_poshta/init_data_order',
                params=params,
                cookies=cookies,
                headers=headers,
            ).json()

            ttn = response.get('data').get('intDocNumber')

            # Если заказ отправлен новой почтой
            if ttn is not None:

                try:
                    ttn = response.get('data').get('intDocNumber')
                except Exception as e:
                    ttn = ''

                try:
                    price = int(response.get('data').get('packageCost'))
                except Exception as e:
                    price = ''

                try:
                    deliveryCost = int(response.get('data').get('deliveryCost'))
                except Exception as e:
                    deliveryCost = ''

            else:
                # Если заказ отправлен укр почтой
                params = {
                    'order_id': f'{id}',
                    'delivery_option_id': '10119216',
                }

                response = requests.get(
                    'https://my.prom.ua/remote/delivery/ukrposhta/init_data_order',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                ).json()

                price = response.get('data').get('declarationId')

                if price is not None:

                    try:
                        ttn = response.get('data').get('declarationId')
                    except Exception as e:
                        ttn = ''

                    try:
                        price = int(response.get('data').get('declaredCost'))
                    except Exception as e:
                        price = ''

                    try:
                        deliveryCost = int(response.get('data').get('deliveryCost'))
                    except Exception as e:
                        deliveryCost = ''

                else:
                    # Если другой способ доставки
                    ttn = ''
                    price = ''
                    deliveryCost = ''

            if len(added_items) > 1:
                # Если в заказе больше одной позиции берем общую цену заказа и ставим в первую позицию
                for item in added_items[:1]:
                    sku = item.get('sku')
                    quantity = item.get('quantity')
                    with open(f'data/orders_list_{month}.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                 id,
                                 order_type,
                                 client_full_name,
                                 payment_option_name,
                                 quantity,
                                 sku,
                                 comments,
                                 ttn,
                                 price,
                                 deliveryCost
                            )
                        )
                # Остальные позици проставляем с ценой и стоиимостью доставки в ноль, что бы не дублировать
                for item in added_items[1:]:
                    sku = item.get('sku')
                    quantity = item.get('quantity')
                    price = 0
                    deliveryCost = 0
                    with open(f'data/orders_list_{month}.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                 id,
                                 order_type,
                                 client_full_name,
                                 payment_option_name,
                                 quantity,
                                 sku,
                                 comments,
                                 ttn,
                                 price,
                                 deliveryCost
                            )
                        )
            else:
                # Если в заказе одна позиция, делаем по стандарту
                for item in added_items:
                    sku = item.get('sku')
                    quantity = item.get('quantity')
                    with open(f'data/orders_list_{month}.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                 id,
                                 order_type,
                                 client_full_name,
                                 payment_option_name,
                                 quantity,
                                 sku,
                                 comments,
                                 ttn,
                                 price,
                                 deliveryCost
                            )
                        )

    # Читаем записанный csv файл и конвертируем его в xlsx
    read_file = pd.read_csv(f'data/orders_list_{month}.csv')

    read_file.to_excel(f'data/order_list_{month}.xlsx', index=None, header=True)


def main():
    get_data(custom_status_id=128816, month='November')


if __name__ == '__main__':
    main()

