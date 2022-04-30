import discord
from utils.logger import *


class Module:
    MODULE_CATEGORY_INFORMATION = "Information"

    def __init__(self, name: str, category: str, description: str = None, examples: list = None):
        self.logger = Logger(Logger.LOG_LEVEL_DEBUG)
        self.name = name
        self.category = category
        self.description = description
        self.examples = examples

    def on_message(self, ctx: discord.Message):
        self.logger.Log(f"Handling command {ctx.content} by user {ctx.author.id} in server {ctx.guild.id}")
