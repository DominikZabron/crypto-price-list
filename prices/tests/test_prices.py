from ..service import parse_prices
from .mocked_response import MOCKED_RESPONSE


def test_parse_prices_succeed():
    expected_result = [
        ('BTC', 3453.70296808),
        ('XRP', 0.299183586734),
        ('ETH', 108.768488507)
    ]
    actual_result = parse_prices(MOCKED_RESPONSE)
    assert expected_result == actual_result
