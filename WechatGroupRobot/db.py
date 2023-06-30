import sqlite3

class SqliteDb:
    # Private static variable to hold the single instance
    __instance = None 

    @staticmethod
    def get_instance():
        if SqliteDb.__instance is None:
            SqliteDb.__instance = SqliteDb('test1.sqlite')
        SqliteDb.__instance.create_table('article', 'hao TEXT, title TEXT, url TEXT, desc TEXT, abst TEXT, ctt TEXT, ctime TEXT DEFAULT CURRENT_TIMESTAMP ')
        return SqliteDb.__instance
    
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.close()

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
        try:
            self.execute(query, list(data.values()))
            self.commit()
        except:
            print(f"!!!!!row create error: {query}")

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

def get_database():
    return SqliteDb.get_instance()

def test():
    db = get_database()
    db.create('article', {
                'title': 'title',
                'hao': 'hao',
                'url': 'xxx',
                'desc': 'desc',
                'abst': '',
                'ctt': 'ctt'
            })
    print(db.read('article', columns=' hao, title, desc, abst, ctt, ctime ', where="url='xxx'"))
    print(db.check_url('xxx'))
    # db.close()

if __name__ == "__main__":
    test()