import discord

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *
from utils.embed import *


class KickMember(Module):
    def __init__(self):
        super().__init__("kick", Module.MODULE_CATEGORY_MODERATION,
                         description="Kick member by mention",
                         examples="<member_ping>")

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if server_config.IsUserAdmin(ctx.author.id):
            try:
                await (await ctx.guild.fetch_member(ParsePing(self.parse.parsedContent[0]).id)).kick()
            except discord.Forbidden:
                await TypicalAnswers.NotEnoughRights("Kick member", ctx)
            else:
                await ctx.reply(embed=Embed(
                    ctx=ctx,
                    title="Kick member",
                    description="Ready, member kicked"
                ))
        else:
            await TypicalAnswers.NeedAdmin("Kick member", ctx)
