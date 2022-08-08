import discord
import psutil
import platform

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys


class Avatar(Module):
    def __init__(self):
        super().__init__("avatar",
                         Module.MODULE_CATEGORY_UTILITY,
                         description="Sends the avatar of a user",
                         examples="<member_ping>")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        if len(ctx.message.mentions) < 1:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="Avatar of user",
                description=f"Invalid usage, please type `{ctx.server_config.prefix}avatar <member_ping>`",
            ))
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title=f"Avatar of {ctx.message.mentions[0].name}",
                description=f"",
            ).set_image(url=(await ParsePing.GetFirstMention(ctx)).avatar_url))
