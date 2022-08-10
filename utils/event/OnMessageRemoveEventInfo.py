import discord

from utils.server_configuration import ServerConfiguration


class OnMessageRemoveEventInfo:
    def __init__(self, ctx: discord.RawMessageDeleteEvent, client: discord.Client, database, bot_config, module):
        self.message = ctx
        self.client = client
        self.database = database
        self.bot_config = bot_config
        self.module = module
