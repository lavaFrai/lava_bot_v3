import discord

from utils.server_configuration import ServerConfiguration


class OnReadyEventInfo:
    def __init__(self, client: discord.Client, database, bot_config, module):
        self.client = client
        self.database = database
        self.bot_config = bot_config
        self.module = module
