from modules.Module import *
from utils.embed import *

import sys

from utils.middleware.backdoorMiddleware import onlyBackdoorMiddleware
from utils.typical_answers import TypicalAnswers


class ServersList(Module):
    def __init__(self):
        super().__init__("serverslist",
                         Module.MODULE_CATEGORY_ADMINISTRATION,
                         description="List of all servers",
                         examples="",
                         visible=False)

    @onlyBackdoorMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        result = f"Bot is member on {len(ctx.client.guilds)} servers\n\n"

        for server in ctx.client.guilds:
            try:
                invite = "No invite"
                # invite = await server.system_channel.create_invite(max_age=300, max_uses=0)
            except discord.Forbidden:
                invite = "Forbidden"
            result += f" `{server.name}` - `{server.id}` by `{(await server.fetch_member(server.owner_id)).name}` \n{invite}\n\n"

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title=ctx.module.title,
            description=result))

