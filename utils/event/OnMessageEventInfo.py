import discord

from utils.server_configuration import ServerConfiguration


class OnMessageEventInfo:
    def __init__(self, ctx: discord.Message, client: discord.Client, database, bot_config, server_config: ServerConfiguration, module):
        self.message = ctx
        self.client = client
        self.database = database
        self.bot_config = bot_config
        self.server_config = server_config
        self.module = module
