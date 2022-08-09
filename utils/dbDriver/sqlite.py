import sqlite3
import pathlib
import os


class BotDatabaseSqlite:
    def __init__(self, configuration):
        self.config = configuration
        self.db = None
        self.ram_cursor = None
        self.ram_db = None
        self.ram_cursor = None

    def init(self):
        self.db = sqlite3.connect(os.path.abspath(self.config["database_host"]))
        self.ram_cursor = self.db.cursor()
        self.ram_db = sqlite3.connect(':memory:')
        self.db.commit()
        self.db.backup(self.ram_db)
        self.ram_db.commit()
        self.ram_cursor = self.ram_db.cursor()

    def get(self, query):
        self.ram_cursor.execute(query)
        return self.ram_cursor.fetchall()

    def send(self, query):
        self.ram_cursor.execute(query)
        self.ram_db.commit()

    def save(self):
        self.ram_db.backup(self.db)
        self.db.commit()

    def selfCheck(self):
        pathlib.Path(self.config['database_host']).parent.mkdir(parents=True, exist_ok=True)
