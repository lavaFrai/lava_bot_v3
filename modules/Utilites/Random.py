import discord
import psutil
import platform
import random

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys


class Random(Module):
    def __init__(self):
        super().__init__("random",
                         Module.MODULE_CATEGORY_UTILITY,
                         description="Returns random number.",
                         examples="100 - random number from 0 to 100 \n"
                                  "100 200 - random number from 100 to 200",
                         aliases=["rand"])

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        from_number = 0
        to_number = 0

        try:
            if len(self.parse.parsedContent) == 0:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    error=True,
                    title="Random",
                    description=f"Invalid usage, please type `{ctx.server_config.prefix}random <from> <to>` or `{ctx.server_config.prefix}random <to>`",
                ))
                return
            elif len(self.parse.parsedContent) == 1:
                to_number = int(self.parse.parsedContent[0])
                from_number = 0

                _from_number = min(from_number, to_number)
                to_number = max(from_number, to_number)
                from_number = _from_number

            elif len(self.parse.parsedContent) >= 2:
                from_number = int(self.parse.parsedContent[0])
                to_number = int(self.parse.parsedContent[1])

                _from_number = min(from_number, to_number)
                to_number = max(from_number, to_number)
                from_number = _from_number

        except ValueError as e:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="Random",
                description=f"Can not parse arguments, please type `{ctx.server_config.prefix}random <from> <to>` or `{ctx.server_config.prefix}random <to>`",
            ))
            return

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title="Random",
            description=f"Random number between {from_number} and {to_number} is `{random.randint(from_number, to_number)}`",
        ))
