import discord
from utils.embed import *


class TypicalAnswers:
    @staticmethod
    async def NeedAdmin(title, ctx: OnMessageEventInfo):
        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            error=True,
            title=title,
            description=f"Sorry, you need a server administrator for this action"
        ))

    @staticmethod
    async def NotEnoughRights(title, ctx: OnMessageEventInfo):
        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            error=True,
            title=title,
            description=f"Error, looks like, not enough rights for this action"
        ))

    @staticmethod
    async def InvalidUsage(title, ctx: OnMessageEventInfo):
        module = ctx.module
        description = ""
        if module.examples is not None:
            description += '```\n'
            for example in module.examples.split('\n'):
                description += f"{ctx.server_config.prefix}{module.name.lower()} {example}\n"
            description += '\n```'
        else:
            description = "*No examples*"

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            error=True,
            title=title,
            description=f"Error, looks like, invalid arguments\nUsage: {description}"
        ))
