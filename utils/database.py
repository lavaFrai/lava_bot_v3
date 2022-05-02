import sqlite3
import os


class BotDatabase:
    def __init__(self, configuration):
        self.config = configuration
        self.db = sqlite3.connect(os.path.abspath("data\\" + configuration["default_database"]))
        self.ram_cursor = self.db.cursor()
        self.ram_db = sqlite3.connect(':memory:')
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
        self.ram_db.commit()
