import json

import discord

from utils.database import *


class ServerConfiguration:
    def __init__(self, id: int, database: BotDatabase, bot_config):
        self.id = id
        self.request = database.get(f"""select * from servers where id='{id}'""")
        if len(self.request) == 0:
            database.send(f"""insert into servers values ('{id}', '{bot_config["default_prefix"]}', '{"[]"}')""")
            database.save()
            self.request = database.get(f"""select * from servers where id='{id}'""")[0]
        self.prefix = self.request[1]
        self.admins = json.JSONDecoder().decode(self.request[2])

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
