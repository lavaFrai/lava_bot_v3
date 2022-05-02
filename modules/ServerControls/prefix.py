import discord

from modules.Module import *


class SetPrefix(Module):
    def __init__(self):
        super().__init__("prefix", Module.MODULE_CATEGORY_ADMINISTRATION)

    async def on_message(self, ctx: discord.Message):
        await ctx.reply("Sorry, wait next update for this function")
