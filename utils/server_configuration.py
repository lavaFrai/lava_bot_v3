import json

import discord

from utils.database import *
from utils.b64 import *


class ServerConfiguration:
    def __init__(self, ctx: discord.Message, database: BotDatabase, bot_config):
        self.id = ctx.guild.id
        self.ctx = ctx
        self.database = database
        self.request = database.get(f"""select * from servers where id='{self.id}'""")
        if len(self.request) == 0:
            database.send(f"""insert into servers values ('{self.id}', '{b64toBytes(bot_config["default_prefix"])}', '{"[]"}')""")
            database.save()
            self.request = database.get(f"""select * from servers where id='{self.id}'""")
        self.request = self.request[0]

        self.prefix = b64fromBytes(self.request[1])
        self.admins: list = json.JSONDecoder().decode(self.request[2])

    def CheckForValidPrefix(self, ctx: discord.Message) -> bool:
        return ctx.content.strip().startswith(self.prefix) or ctx.content.strip().startswith(f"<@{ctx.guild.me.id}>")

    def GetCommandText(self, ctx: discord.Message) -> str:
        message = str(ctx.content)
        lPtr = 0
        _prefix = self.prefix

        # skipping prefix
        if message.startswith(_prefix):
            lPtr = len(_prefix)
        else:
            lPtr = message.find('>') + 1
        if lPtr >= len(message):
            return ""

        # skipping whitespace
        while (lPtr < len(message)) and (message[lPtr] in ' \n\t\r'):
            lPtr += 1

        # reading keyword
        rPtr = lPtr
        while (rPtr < len(message)) and (message[rPtr] not in ' \n\t\r'):
            rPtr += 1

        return message[lPtr:rPtr]

    def GetRealText(self, ctx: discord.Message) -> str:
        message = str(ctx.content)
        lPtr = 0
        _prefix = self.prefix

        # skipping prefix
        if message.startswith(_prefix):
            lPtr = len(_prefix)
        else:
            lPtr = message.find('>') + 1
        if lPtr >= len(message):
            return ""

        # skipping whitespace
        while (lPtr < len(message)) and (message[lPtr] in ' \n\t\r'):
            lPtr += 1

        # reading keyword
        rPtr = lPtr
        while (rPtr < len(message)) and (message[rPtr] not in ' \n\t\r'):
            rPtr += 1

        return message[rPtr:]

    def SetNewPrefix(self, prefix: str):
        self.database.send(f"""update servers set prefix='{b64toBytes(prefix)}' where id='{self.id}'""")
        self.database.save()
        self.prefix = prefix

    def IsUserAdmin(self, user_id: int):
        return user_id in self.admins or user_id == self.ctx.guild.owner_id

    def AddAdministrator(self, id: int):
        self.database.send(f"""update servers set admin='{json.JSONEncoder().encode(self.admins + [id])}' where id='{self.id}'""")
        self.database.save()
        self.admins += [id]

    def RemoveAdministrator(self, id: int):
        self.admins.remove(id)
        self.database.send(f"""update servers set admin='{json.JSONEncoder().encode(self.admins)}' where id='{self.id}'""")
        self.database.save()
