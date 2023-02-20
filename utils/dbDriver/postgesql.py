import base64

import psycopg2
from psycopg2 import errors as pg_errors
import os
from utils.dbDriver.driver import IDatabaseDriver
import datetime


class BotDatabasePostgresql(IDatabaseDriver):
    def __init__(self, configuration):
        self.config = configuration
        self.db = None
        self.cursor = None

    def init(self):
        self.db = psycopg2.connect(dbname=self.config['database_name'], user=self.config['database_user'],
                                   password=self.config['database_password'], host=self.config['database_host'])
        self.cursor = self.db.cursor()

    """def get_threadsafe(self, query, args=None):
        from __main__ import server

        if type(args) != tuple:
            args = (args,)
        server.eventManager.send("database:get", f"{base64.b64encode(query.encode()).decode()}:{base64.b64encode(str(args).encode()).decode()}:{os.getpid()}")
        res = eval(base64.b64decode(server.eventManager.unconcurent_wait(f"database:get:{os.getpid()}")))
        return res"""

    """def send_threadsafe(self, query, args=None):
        from __main__ import server

        if type(args) != tuple:
            args = (args,)
        server.eventManager.send("database:send", f"{base64.b64encode(query.encode()).decode()}:{base64.b64encode(str(args).encode()).decode()}:{os.getpid()}")
        res = server.eventManager.unconcurent_wait(f"database:send:{os.getpid()}")
        return {}"""

    def get(self, query, args=None):
        if type(args) != tuple:
            args = (args,)
        cursor = self.db.cursor()

        try:
            if args is None:
                cursor.execute(query)
            else:
                cursor.execute(query, args)
        except pg_errors.InFailedSqlTransaction:
            self.db.rollback()
        return cursor.fetchall()

        # return self.get_threadsafe(query, args)

    """
        if type(args) != tuple:
            args = (args,)
        try:
            if args is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, args)
        except pg_errors.InFailedSqlTransaction:
            self.db.rollback()
        return self.cursor.fetchall()
    """

    # def get_real(self, query, args=None):
    #     if type(args) != tuple:
    #         args = (args,)
    #     try:
    #         if args is None:
    #             self.cursor.execute(query)
    #         else:
    #             self.cursor.execute(query, args)
    #     except pg_errors.InFailedSqlTransaction:
    #         self.db.rollback()
    #     try:

    #         return self.cursor.fetchall()
    #     except pg_errors.ProgrammingError:
    #         return self.get_real(query, args)

    def send(self, query, args=None):
        cursor = self.db.cursor()

        if type(args) != tuple:
            args = (args,)

        try:
            if args is None:
                self.cursor.execute(query)
            else:
                self.cursor.execute(query, args)
            self.db.commit()
        except pg_errors.InFailedSqlTransaction:
            self.db.rollback()

    # def send_real(self, query, args=None):
    #     if type(args) != tuple:
    #         args = (args,)
    #
    #     try:
    #         if args is None:
    #             self.cursor.execute(query)
    #         else:
    #             self.cursor.execute(query, args)
    #         self.db.commit()
    #     except pg_errors.InFailedSqlTransaction:
    #         self.db.rollback()

    def save(self):
        self.db.commit()

    def selfCheck(self):
        pass
