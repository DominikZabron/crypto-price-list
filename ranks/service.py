import requests
import json
import time
import logging
import os

WEBAPI_URL = 'http://web-api:8000/ranks'
REQUEST_URL = 'https://min-api.cryptocompare.com/data/top/mktcap?&limit_toplist=200&limit=100&tsym=USD&page='
REQUEST_HEADERS = {'Apikey': os.getenv('CRYPTOCOMPARE_KEY')}


def fetch_ranks(page):
    """
    Request for actual rank of most market capitalized coins.

    :param page: int
    :return: response data or None
    """
    resp = requests.get(REQUEST_URL + str(page), headers=REQUEST_HEADERS)
    return resp.text


def parse_ranks(raw, page):
    """
    Parse raw response from cryptocompare API

    Give ranks based on the order and page.

    Example body:
    {
        "Message": "Success",
        "Type": 100,
        "SponsoredData": [],
        "Data": [
            {
                "CoinInfo": {
                    "Id": "1182",
                    "Name": "BTC",
                    "FullName": "Bitcoin",
                    "Internal": "BTC",
                    "ImageUrl": "/media/19633/btc.png",
                    "Url": "/coins/btc/overview",
                    "Algorithm": "SHA256",
                    "ProofType": "PoW",
                    "NetHashesPerSecond": 41623606545.7453,
                    "BlockNumber": 562156,
                    "BlockTime": 600,
                    "BlockReward": 12.5,
                    "Type": 1,
                    "DocumentType": "Webpagecoinp"
                },
                "ConversionInfo": {
                    "Conversion": "direct",
                    "ConversionSymbol": "",
                    "CurrencyFrom": "BTC",
                    "CurrencyTo": "USD",
                    "Market": "CCCAGG",
                    "Supply": 17526962,
                    "TotalVolume24H": 262460.9017932329,
                    "SubBase": "5~",
                    "SubsNeeded": [
                        "5~CCCAGG~BTC~USD"
                    ],
                    "RAW": [
                        "5~CCCAGG~BTC~USD~4~3442.37~1549635867~0.18074517~634.361323149~336784707~28880.956998999554~98616978.56160338~40068.3894317765~136409878.8012065~3375.3~3448.15~3363.32~3393.43~3451.84~3366.72~Bitfinex~1935.8583130503964~6640981.240057511~3434.11~3448.15~3433.88~ffffe9"
                    ]
                }
            },
        ],
        "RateLimit": {},
        "HasWarning": false
    }

    Exapmple response:
    [('BTC', 1), ('XRP', 2), ... , ('QRL', 200)]

    :param raw: response body
    :param page: int
    :return: list of symbols with rank
    """
    ranks = []
    payload = json.loads(raw)

    inc = 1 if page == 0 else 101

    for rank, item in enumerate(payload.get('Data', {})):
        ranks.append(
            (item['ConversionInfo']['CurrencyFrom'].replace('*', ''), rank + inc))

    return ranks


def update_ranks(ranks):
    """Send the request with new ranks to update."""
    resp = requests.put(WEBAPI_URL, data=json.dumps(ranks))
    logging.info(resp.status_code)


def run():
    """Fetch new ranks, parse the response, apply ranks and send request with update."""
    ranks = []

    for page in range(2):
        payload = fetch_ranks(page)
        ranks += parse_ranks(payload, page)

    update_ranks(ranks)


if __name__ == "__main__":
    while True:
        run()
        time.sleep(180)  # 3 minutes
