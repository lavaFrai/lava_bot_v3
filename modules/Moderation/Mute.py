import discord

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *
from utils.time_parser import *


class MuteMember(Module):
    def __init__(self):
        super().__init__("mute", Module.MODULE_CATEGORY_MODERATION)

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if server_config.IsUserAdmin(ctx.author.id):
            try:
                mute_member: discord.Member = await ctx.guild.fetch_member(ParsePing(self.parse.parsedContent[0]).id)
                mute_time = ParseTime(self.parse.parsedContent[1])
                await mute_member.timeout(duration=mute_time.time.s)
            except discord.Forbidden:
                await TypicalAnswers.NotEnoughRights("Mute member", ctx)
            else:
                await ctx.reply(embed=discord.Embed(
                    title="Mute member",
                    description=f"Ready, member muted for {mute_time.time.s}s"
                ))
        else:
            await TypicalAnswers.NeedAdmin("Mute member", ctx)
