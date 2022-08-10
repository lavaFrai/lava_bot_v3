from modules.Module import *
from utils.ping_parser import *
from utils.embed import *
from utils.middleware.sudoMiddleware import *


class KickMember(Module):
    def __init__(self):
        super().__init__("kick", Module.MODULE_CATEGORY_MODERATION,
                         description="Kick member by mention",
                         examples="<member_ping>",
                         title="Kick member")

    @onlySudoMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        try:
            await (await ctx.message.guild.fetch_member(ParsePing(self.parse.parsedContent[0]).id)).kick()
        except discord.Forbidden:
            await TypicalAnswers.NotEnoughRights("Kick member", ctx)
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Kick member",
                description="Ready, member kicked"
            ))
