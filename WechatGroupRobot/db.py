import sqlite3

class SqliteDb:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

    def execute(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
    
    def commit(self):
        self.conn.commit()

    def create_table(self, table_name, columns):
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns}, PRIMARY KEY(url))"
        self.execute(query)
        self.commit()

    def create(self, table, data):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.execute(query, list(data.values()))
        self.commit()

    def read(self, table, columns=None, where=None, params=None):
        if not columns:
            columns = '*'
        query = f'SELECT {columns} FROM {table}'
        if where:
            query += f' WHERE {where}'
        self.execute(query, params)
        return self.fetchall()
    
    def check_url(self, url_to_check):
        # url_to_check = 'https://example.com/article1'
        query = f"SELECT * FROM article WHERE url = '{url_to_check}'"
        self.execute(query)
        result = self.fetchone()
        return result is not None


def test():
    # db = SqliteDb('test.db')
    # db.create_table('article1', 'hao TEXT, title TEXT, url TEXT, desc TEXT, abst TEXT, ctt TEXT')
    # db.close()


    db = SqliteDb('test.db')
    # db.create('article1', {
    #     'title': 'test',
    #     'hao': 'xxx',
    #     'url': 'xxx',
    #     'desc': 'xxx',
    #     'abst': 'xxx',
    #     'ctt': 'xxx'
    # })
    print(db.read('article1', columns=' hao, title, desc, abst, ctt ', where="url='xxx'"))
    print(db.check_url('xxx'))
    db.close()

if __name__ == "__main__":
    test()