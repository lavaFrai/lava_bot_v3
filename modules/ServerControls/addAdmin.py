import discord

from modules.Module import *
from utils.message_parser import *
from utils.server_configuration import *
from utils.ping_parser import ParsePing
from utils.embed import *


class AdminControls(Module):
    def __init__(self):
        super().__init__("admin", Module.MODULE_CATEGORY_ADMINISTRATION,
                         description="Add, remove or show list of administrators",
                         examples="list\n"
                                  "add <member_ping>\n"
                                  "remove <member_ping>")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)
        if ctx.server_config.IsUserAdmin(ctx.message.author.id):
            if len(self.parse) == 0:
                await ctx.message.reply(embed=Embed(
                    error=True,
                    ctx=ctx,
                    title="Administrator controls",
                    description=f"Type `{ctx.server_config.prefix} admin [add / remove / list]`"
                ))
            else:
                if len(self.parse) == 1:
                    if self.parse.parsedContentLower[0] == "list":
                        await ctx.message.reply(embed=Embed(
                            ctx=ctx,
                            title="Server admins list",
                            description="Current server admins:\n" + "\n".join(
                                [f"<@{i}>" for i in ctx.server_config.admins + [ctx.message.guild.owner_id]]) + "\n"
                        ))
                    else:
                        await ctx.message.reply(embed=Embed(
                            error=True,
                            ctx=ctx,
                            title="Administrator controls",
                            description=f"Type `{ctx.server_config.prefix} admin [add / remove] <member ping>`"
                        ))
                else:
                    try:
                        user = ParsePing(self.parse.parsedContent[1])
                    except BaseException:
                        await ctx.message.reply(embed=Embed(
                            ctx=ctx,
                            error=True,
                            title="Administrator controls",
                            description=f"Type `{ctx.server_config.prefix} admin [add / remove] <member ping>`"
                        ))
                    else:
                        if user.id == ctx.client.user.id:
                            await ctx.message.reply(embed=Embed(
                                ctx=ctx,
                                error=True,
                                title="Administrator controls",
                                description=f"Error, i'm unconditional server admin"
                            ))
                        elif user.id == ctx.message.guild.owner_id:
                            await ctx.message.reply(embed=Embed(
                                ctx=ctx,
                                error=True,
                                title="Administrator controls",
                                description=f"Error, <@{user.id}> already server owner"
                            ))
                        else:
                            if self.parse.parsedContentLower[0] == "list":
                                await ctx.message.reply(embed=Embed(
                                    ctx=ctx,
                                    title="Server admins list",
                                    description="Current server admins:\n" + "\n".join(
                                        [f"<@{i}>" for i in ctx.server_config.admins + [ctx.message.guild.owner_id]]) + "\n"
                                ))
                            elif self.parse.parsedContentLower[0] == "add":
                                if user.id in ctx.server_config.admins:
                                    await ctx.message.reply(embed=Embed(
                                        ctx=ctx,
                                        error=True,
                                        title="Administrator controls",
                                        description=f"Error, <@{user.id}> already server admin"
                                    ))
                                else:
                                    ctx.server_config.AddAdministrator(user.id)
                                    await ctx.message.reply(embed=Embed(
                                        ctx=ctx,
                                        title="New administrator",
                                        description=f"Ready, {self.parse.parsedContent[1]} is new administrator"
                                    ))
                            elif self.parse.parsedContentLower[0] == "remove":
                                if user.id not in ctx.server_config.admins:
                                    await ctx.message.reply(embed=Embed(
                                        ctx=ctx,
                                        error=True,
                                        title="Administrator controls",
                                        description=f"Error, <@{user.id}> isn't server admin"
                                    ))
                                else:
                                    ctx.server_config.RemoveAdministrator(user.id)
                                    await ctx.message.reply(embed=Embed(
                                        ctx=ctx,
                                        title="Remove administrator",
                                        description=f"Ready, {self.parse.parsedContent[1]} is no longer an administrator"
                                    ))
        else:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="Administrator controls",
                description=f"Sorry, you need a server administrator for this action"
            ))
