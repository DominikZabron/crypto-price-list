import pytest


@pytest.fixture
def database():
    from ..db import Storage
    return Storage()


def test_database_init_has_table_prices(database):
    name = 'prices'
    database.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(name))
    assert database.cursor.fetchone() == (name,)


def test_database_init_has_table_ranks(database):
    name = 'ranks'
    database.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(name))
    assert database.cursor.fetchone() == (name,)


def test_database_init_has_view_ranked_prices(database):
    name = 'ranked_prices'
    database.cursor.execute(
        """
        SELECT name FROM sqlite_master 
        WHERE type='view' AND name='{}'
        """.format(name))
    assert database.cursor.fetchone() == (name,)


def test_update_ranks_successful(database):
    ranks = [('BTC', 1), ('XRP', 2), ('ETH', 3)]
    database.update_ranks(ranks)
    database.cursor.execute("SELECT symbol, rank FROM ranks")
    assert database.cursor.fetchall() == ranks


def test_update_prices_successful(database):
    prices = [('BTC', 3453.70296808), ('XRP', 0.299183586734), ('ETH', 108.768488507)]
    database.update_prices(prices)
    database.cursor.execute("SELECT symbol, price FROM prices")
    assert database.cursor.fetchall() == prices


def test_get_ranked_prices_successful(database):
    expected_ranked_prices = [
        ('BTC', 1, 3453.70296808),
        ('XRP', 2, 0.299183586734),
        ('ETH', 3, 108.768488507)
    ]
    ranks = [('BTC', 1), ('XRP', 2), ('ETH', 3)]
    prices = [('BTC', 3453.70296808), ('XRP', 0.299183586734), ('ETH', 108.768488507)]
    database.update_ranks(ranks)
    database.update_prices(prices)
    actual_ranked_prices = database.get_ranked_prices(limit=10)
    assert expected_ranked_prices == actual_ranked_prices