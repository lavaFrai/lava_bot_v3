import discord

from modules.Module import *


class DebugInfo(Module):
    def __init__(self):
        super().__init__("debuginfo", Module.MODULE_CATEGORY_INFORMATION)

    async def on_message(self, ctx: discord.Message):
        super().on_message(ctx)

        await ctx.reply(embed=discord.Embed(
            title="Debug Information",
            description=f"Guild id: {ctx.guild.id}\n"
                        f"Author id: {ctx.author.id}\n"
                        f"Message id: {ctx.id}\n"
        ))
