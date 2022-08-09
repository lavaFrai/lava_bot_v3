import discord
from utils.logger import *
from utils.message_parser import *
from utils.server_configuration import *
from modules.OnMessageEventInfo import *


class Module:
    MODULE_CATEGORY_INFORMATION = "Information"
    MODULE_CATEGORY_MODERATION = "Moderation"
    MODULE_CATEGORY_ADMINISTRATION = "Administration"
    MODULE_CATEGORY_NSFW = "NSFW"
    MODULE_CATEGORY_FUN = "Fun"
    MODULE_CATEGORY_UTILITY = "Utility"

    def __init__(self, name: str, category: str, description: str = None, examples: list = None, aliases=None, title: str = None):
        self.logger = Logger(Logger.LOG_LEVEL_DEBUG)
        self.name = name
        self.category = category
        self.description = description
        self.examples: str = examples
        self.parse: MessageParser = None

        self.aliases = aliases
        if aliases is not None:
            self.aliases = list(map(lambda x: x.lower(), aliases))

        self.title = title
        if title is None:
            self.title = name.capitalize()

    def IsAliasFor(self, name: str) -> bool:
        if self.aliases is None:
            return name.lower() == self.name
        return name.lower() in self.aliases or name.lower() == self.name

    def on_message(self, ctx: OnMessageEventInfo):
        self.parse = MessageParser(ctx)
        self.logger.Log(f"Handling command {ctx.message.content} by user {ctx.message.author.id} on server {ctx.message.guild.id}")
