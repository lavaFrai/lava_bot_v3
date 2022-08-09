import psycopg2
import os


class BotDatabasePostgresql:
    def __init__(self, configuration):
        self.config = configuration
        self.db = None
        self.cursor = None

    def init(self):
        self.db = psycopg2.connect(dbname=self.config['database_name'], user=self.config['database_user'],
                                   password=self.config['database_password'], host=self.config['database_host'])
        self.cursor = self.db.cursor()

    def get(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def send(self, query):
        self.cursor.execute(query)
        self.db.commit()

    def save(self):
        self.db.commit()

    def selfCheck(self):
        pass
