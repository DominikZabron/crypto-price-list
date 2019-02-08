from ..service import parse_ranks
from .mocked_response import MOCKED_RESPONSE


def test_parse_ranks_succeed():
    expected_result = [('BTC', 1), ('XRP', 2), ('ETH', 3)]
    actual_result = parse_ranks(MOCKED_RESPONSE, 0)
    assert expected_result == actual_result
