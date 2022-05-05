import pymysql
class UseDatebase:
    def __init__(self, config:dict):
        self.config = config

    def __enter__(self):
        self.conn = pymysql.connect(**self.config)
        self.corsor = self.conn.cursor()
        return self.corsor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.corsor.close()
        self.conn.close()

