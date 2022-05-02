import discord
from modules.Information.debuginfo import DebugInfo
from modules.ServerControls.prefix import SetPrefix
from utils.server_configuration import *


class ModuleManager:
    def __init__(self):
        self.Modules = list()
        self.Categories = set()

        # Administration
        self.Modules.append(SetPrefix())
        # Information
        self.Modules.append(DebugInfo())

        for i in self.Modules:
            self.Categories.add(i.category)

    def getModule(self, name: str):
        for i in self.Modules:
            if i.name == name:
                return i
        return None

    async def on_help(self, ctx: discord.Message, server_config: ServerConfiguration):
        description = ""
        for category_name in self.Categories:
            description += f"\n**{category_name}**\n"
            for module in filter(lambda x: x.category == category_name, self.Modules):
                description += f"`{server_config.prefix}{module.name}` "

        await ctx.reply(embed=discord.Embed(
            title="Available commands:",
            description=description
        ))
