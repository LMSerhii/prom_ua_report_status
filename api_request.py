import json

import pprint
import requests


from auth_data import apiKey_np, my_phone, PRODUCTION_BEARER_StatusTracking
from repeat import request_test


def send_request_to_np(ttn):
    """  """
    url = 'https://api.novaposhta.ua/v2.0/json/'

    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}

    data = {
        "apiKey": apiKey_np,
        "modelName": "TrackingDocument",
        "calledMethod": "getStatusDocuments",
        "methodProperties": {
            "Documents": [
                {
                    "DocumentNumber": f"{ttn}",
                    "Phone": my_phone
                }
                        ]
                            }
            }

    # response = requests.post(url, data=json.dumps(data), headers=headers).json()

    response = request_test(
        url=url,
        method='post',
        data=json.dumps(data),
        headers=headers
    ).json()

    return response


def send_request_to_ukr(ttn):
    """ """
    headers = {
        'Authorization': f'Bearer {PRODUCTION_BEARER_StatusTracking}',
        'Content-Type': 'application/json',
    }
    url = f'https://www.ukrposhta.ua/status-tracking/0.0.1/statuses/last?barcode={ttn}'

    # response = requests.get(url=url, headers=headers).json()

    response = request_test(
        url=url,
        method='get',
        headers=headers,
    ).json()

    return response


def main():
    ttn_number = input('Enter ttn number: ')
    pprint.pprint(send_request_to_np(ttn=ttn_number))
    # pprint.pprint(send_request_to_ukr(ttn=ttn_number))


if __name__ == '__main__':
    main()