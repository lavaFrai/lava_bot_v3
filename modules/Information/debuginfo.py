import discord

from modules.Module import *


class DebugInfo(Module):
    def __init__(self):
        super().__init__("debuginfo", Module.MODULE_CATEGORY_INFORMATION)

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        await ctx.reply(embed=discord.Embed(
            title="Debug Information",
            description=f"Guild id: {ctx.guild.id}\n"
                        f"Author id: {ctx.author.id}\n"
                        f"Message id: {ctx.id}\n"
        ))
