import discord

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *
from utils.embed import *
from utils.sudoMiddleware import *


class BanMember(Module):
    def __init__(self):
        super().__init__("ban", Module.MODULE_CATEGORY_MODERATION,
                         description="Ban member by mention",
                         examples="<member_ping>",
                         title="Ban member")

    @onlySudoMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        try:
            await (await ctx.message.guild.fetch_member(ParsePing(self.parse.parsedContent[0]).id)).ban()
        except discord.Forbidden:
            await TypicalAnswers.NotEnoughRights("Ban member", ctx)
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Ban member",
                description="Ready, member banned"
            ))
