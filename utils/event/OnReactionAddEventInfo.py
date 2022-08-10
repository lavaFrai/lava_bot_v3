import discord

from utils.server_configuration import ServerConfiguration


class OnReactionAddEventInfo:
    def __init__(self, ctx: discord.RawReactionActionEvent, client: discord.Client, database, bot_config, module):
        self.reaction = ctx
        self.client = client
        self.database = database
        self.bot_config = bot_config
        self.guild: discord.Guild = client.get_guild(ctx.guild_id)
        self.message = None
        self.module = module
