import discord
from utils.logger import *
from utils.message_parser import *
from utils.database import *
from utils.server_configuration import *


class Module:
    MODULE_CATEGORY_INFORMATION = "Information"
    MODULE_CATEGORY_MODERATION = "Moderation"
    MODULE_CATEGORY_ADMINISTRATION = "Administration"
    MODULE_CATEGORY_NSFW = "NSFW"

    def __init__(self, name: str, category: str, description: str = None, examples: list = None, aliases=None):
        self.logger = Logger(Logger.LOG_LEVEL_DEBUG)
        self.name = name
        self.category = category
        self.description = description
        self.examples = examples
        self.parse: MessageParser = None
        self.aliases = aliases
        if aliases is not None:
            self.aliases = list(map(lambda x: x.lower(), aliases))

    def IsAliasFor(self, name: str) -> bool:
        if self.aliases is None:
            return name.lower() == self.name
        return name.lower() in self.aliases or name.lower() == self.name

    def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        self.parse = MessageParser(ctx, server_config)
        self.logger.Log(f"Handling command {ctx.content} by user {ctx.author.id} on server {ctx.guild.id}")
