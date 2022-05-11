from modules.Module import *
from utils.server_configuration import *


class DemoModule(Module):
    def __init__(self):
        super().__init__("test", "Demo")

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config, server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if server_config.IsUserAdmin(ctx.author.id):
            server_config.SetNewPrefix(self.parse.parsedContent[0])
            await ctx.reply(embed=discord.Embed(
                title="Demonstration",
                description=f"Hello, admin!"
            ))
        else:
            await ctx.reply(embed=discord.Embed(
                title="Demonstration",
                description=f"Hello, member!"
            ))
