import requests
import json
import logging
import time
import os

WEBAPI_URL = 'http://web-api:8000/prices'
REQUEST_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=300'
REQUEST_HEADERS = {'X-CMC_PRO_API_KEY': os.getenv('COINMARKETCAP_KEY')}


def fetch_prices():
    """
    Request for actual prices of most market capitalized coins.

    :return: response data or None
    """
    resp = requests.get(REQUEST_URL, headers=REQUEST_HEADERS)

    if resp.status_code == 200:
        return resp.text


def parse_prices(raw):
    """
    Parse raw response from coinmarketcap API.

    Example body:
    {
        "status": {
            "timestamp": "2019-02-08T12:56:52.772Z",
            "error_code": 0,
            "error_message": null,
            "elapsed": 7,
            "credit_count": 1
        },
        "data": [
            {
                "id": 1,
                "name": "Bitcoin",
                "symbol": "BTC",
                "slug": "bitcoin",
                "circulating_supply": 17526900,
                "total_supply": 17526900,
                "max_supply": 21000000,
                "date_added": "2013-04-28T00:00:00.000Z",
                "num_market_pairs": 6600,
                "tags": [
                    "mineable"
                ],
                "platform": null,
                "cmc_rank": 1,
                "last_updated": "2019-02-08T12:56:26.000Z",
                "quote": {
                    "USD": {
                        "price": 3453.29201346,
                        "volume_24h": 5513059982.85242,
                        "percent_change_1h": 0.145325,
                        "percent_change_24h": 1.11952,
                        "percent_change_7d": -0.43863,
                        "market_cap": 60525503790.712074,
                        "last_updated": "2019-02-08T12:56:26.000Z"
                    }
                }
            }
        ]
    }

    Example return:
    [('BTC', 3450.22714956), ('XRP', 0.298489261075), ... ,('ETH', 108.606675153)]

    :param raw: response body
    :return: list of symbols with prices
    """
    prices = []
    payload = json.loads(raw)

    for item in payload.get('data', {}):
        prices.append((item['symbol'], item['quote']['USD']['price']))

    return prices


def update_prices(prices):
    """Send the request with new prices to update."""
    resp = requests.put(WEBAPI_URL, data=json.dumps(prices))
    logging.info(resp.status_code)


def run():
    """Fetch new prices, parse the response and send request with update."""
    payload = fetch_prices()
    prices = parse_prices(payload)
    update_prices(prices)


if __name__ == "__main__":
    while True:
        run()
        time.sleep(180)  # 3 minutes
