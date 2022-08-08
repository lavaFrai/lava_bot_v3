import discord

from modules.Module import *
from utils.message_parser import *
from utils.database import *
from utils.server_configuration import *
from utils.embed import *


class SetPrefix(Module):
    def __init__(self):
        super().__init__("prefix", Module.MODULE_CATEGORY_ADMINISTRATION,
                         description="Set new bot prefix for this server",
                         examples="<new_prefix>")

    async def on_message(self, ctx: OnMessageEventInfo):
        parsed_content = MessageParser(ctx)

        if len(parsed_content) == 0:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Server prefix",
                description=f"Current server prefix is `{ctx.server_config.prefix}`\n"
                            f"Type `{ctx.server_config.prefix}prefix <new prefix>` to set new prefix"
            ))
        else:
            if ctx.server_config.IsUserAdmin(ctx.message.author.id):
                ctx.server_config.SetNewPrefix(self.parse.parsedContent[0])
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    title="Server prefix",
                    description=f"Ready, current server prefix is `{ctx.server_config.prefix}`\n"
                                f"Type `{ctx.server_config.prefix}prefix <new prefix>` to set new prefix"
                ))
            else:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    error=True,
                    title="Server prefix",
                    description=f"Sorry, you need a server administrator for this action"
                ))
