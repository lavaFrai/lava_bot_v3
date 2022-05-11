import discord

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *


class BanMember(Module):
    def __init__(self):
        super().__init__("ban", Module.MODULE_CATEGORY_MODERATION)

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if server_config.IsUserAdmin(ctx.author.id):
            try:
                await (await ctx.guild.fetch_member(ParsePing(self.parse.parsedContent[0]).id)).ban()
            except discord.Forbidden:
                await TypicalAnswers.NotEnoughRights("Ban member", ctx)
            else:
                await ctx.reply(embed=discord.Embed(
                    title="Ban member",
                    description="Ready, member banned"
                ))
        else:
            await TypicalAnswers.NeedAdmin("Ban member", ctx)
