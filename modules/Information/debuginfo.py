import discord

from modules.Module import *
from utils.embed import *


class DebugInfo(Module):
    def __init__(self):
        super().__init__("debuginfo", Module.MODULE_CATEGORY_INFORMATION)

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title="Debug Information",
            description=f"Guild id: {ctx.message.guild.id}\n"
                        f"Author id: {ctx.message.author.id}\n"
                        f"Message id: {ctx.message.id}\n"
        ))
