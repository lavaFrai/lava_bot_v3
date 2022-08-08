from modules.Module import *
from utils.server_configuration import *
from utils.embed import *


class DemoModule(Module):
    def __init__(self):
        super().__init__("test", "Demo",
                         description="Demonstration module",
                         examples="<arg1> - and about it \n"
                                  "<arg1> <arg2>")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        if ctx.server_config.IsUserAdmin(ctx.message.author.id):
            ctx.server_config.SetNewPrefix(self.parse.parsedContent[0])
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Demonstration",
                description=f"Hello, admin!"
            ))
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Demonstration",
                description=f"Hello, member!"
            ))
