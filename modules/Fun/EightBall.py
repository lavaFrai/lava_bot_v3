import discord
import psutil
import platform
import random

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys


class EightBall(Module):
    def __init__(self):
        super().__init__("8ball",
                         Module.MODULE_CATEGORY_FUN,
                         description="Gives you the only right answers to any of your questions (but I'm not sure, hehe).",
                         examples="<question>")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        answers = [
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]

        parsed_content = MessageParser(ctx)
        try:
            bet = parsed_content[0].lower()
        except IndexError:
            bet = ""

        if bet == "":
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="8ball",
                description=f"Invalid usage, please type `{ctx.server_config.prefix}8ball <question>`",
            ))
            return

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title="Coin",
            description=f"To your question `{' '.join(parsed_content)}`\n"
                        f"8ball says: `{random.choice(answers)}`",
        ))
