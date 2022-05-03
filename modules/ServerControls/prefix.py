import discord

from modules.Module import *
from utils.message_parser import *
from utils.database import *
from utils.server_configuration import *


class SetPrefix(Module):
    def __init__(self):
        super().__init__("prefix", Module.MODULE_CATEGORY_ADMINISTRATION)

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if len(self.parse) == 0:
            await ctx.reply(embed=discord.Embed(
                title="Server prefix",
                description=f"Current server prefix is `{server_config.prefix}`\n"
                            f"Type `{server_config.prefix} prefix <new prefix>` to set new prefix"
            ))
        else:
            if server_config.IsUserAdmin(ctx.author.id):
                server_config.SetNewPrefix(self.parse.parsedContent[0])
                await ctx.reply(embed=discord.Embed(
                    title="Server prefix",
                    description=f"Ready, current server prefix is `{server_config.prefix}`\n"
                                f"Type `{server_config.prefix} prefix <new prefix>` to set new prefix"
                ))
            else:
                await ctx.reply(embed=discord.Embed(
                    title="Server prefix",
                    description=f"Sorry, you need a server administrator for this action"
                ))


