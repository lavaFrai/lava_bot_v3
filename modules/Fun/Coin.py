import discord
import psutil
import platform
import random

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys


class Coin(Module):
    def __init__(self):
        super().__init__("coin",
                         Module.MODULE_CATEGORY_FUN,
                         description="Flips a coin and tells you if your guess was right.",
                         examples="<your_ask>")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        parsed_content = MessageParser(ctx)
        try:
            bet = parsed_content[0].lower()
        except IndexError:
            bet = ""

        if bet not in ["heads", "tails"]:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="Coin",
                description=f"Invalid usage, please type `{ctx.server_config.prefix}coin <heads/tails>`",
            ))
            return

        if random.randint(0, 1) == 1:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Coin",
                description=f"The coin landed on `{bet}` and **you won!**",
            ))
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Coin",
                description=f"The coin landed on `{bet}` and **you lost!**",
            ))
