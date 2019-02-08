import sqlite3


class Storage(object):
    def __init__(self):
        conn = sqlite3.connect(':memory:')
        self.cursor = conn.cursor()
        self.cursor.execute(
            """
            CREATE TABLE ranks (
              symbol text PRIMARY KEY,
              rank integer
            );
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE prices (
              symbol text PRIMARY KEY,
              price numeric
            );
            """
        )
        self.cursor.execute(
            """
            CREATE VIEW ranked_prices 
            AS 
            SELECT r.symbol, r.rank, p.price
            FROM ranks r 
            LEFT JOIN prices p 
              ON r.symbol = p.symbol
            ORDER BY r.rank;
            """
        )

    def update_ranks(self, ranks):
        self.cursor.executemany('INSERT OR REPLACE INTO ranks VALUES (?, ?)', ranks)

    def update_prices(self, prices):
        self.cursor.executemany('INSERT OR REPLACE INTO prices VALUES (?, ?)', prices)

    def get_ranked_prices(self, limit):
        self.cursor.execute(f'SELECT symbol, rank, price FROM ranked_prices LIMIT {limit}')
        return self.cursor.fetchall()
