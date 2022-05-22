import discord
from utils.embed import *


class TypicalAnswers:
    @staticmethod
    async def NeedAdmin(title, ctx: discord.Message):
        await ctx.reply(embed=Embed(
            ctx=ctx,
            error=True,
            title=title,
            description=f"Sorry, you need a server administrator for this action"
        ))

    @staticmethod
    async def NotEnoughRights(title, ctx: discord.Message):
        await ctx.reply(embed=Embed(
            ctx=ctx,
            error=True,
            title=title,
            description=f"Error, looks like, not enough rights for this action"
        ))
