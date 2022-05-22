import random

import discord
import hmtai

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *
from utils.hentai import *
from utils.embed import *


class Hentai(Module):
    def __init__(self):
        super().__init__("hentai", Module.MODULE_CATEGORY_NSFW,
                         aliases=["hent"])

    async def on_message(self, ctx: discord.Message, client: discord.Client, database: BotDatabase, bot_config,
                         server_config: ServerConfiguration):
        super().on_message(ctx, client, database, bot_config, server_config)

        if not ctx.channel.is_nsfw():
            await ctx.reply(embed=Embed(ctx=ctx,
                                        error=True,
                                        title="Hentai",
                                        description=f"Sorry, i can't send that in this channel, it is not NSFW channel"))
            return

        hentai = HentaiGenerator()

        if len(self.parse) == 0:
            await ctx.reply(embed=Embed(
                ctx=ctx,
                title="Hentai"
            ).set_image(
                url=hentai.GetRandomUrl()
            ))
        else:
            if self.parse.parsedContent[0] in hentai.possible:
                await ctx.reply(embed=Embed(
                    ctx=ctx,
                    title="Hentai",
                    description=self.parse.parsedContent[0]
                ).set_image(
                    url=hentai.GetRandomUrl(self.parse.parsedContent[0])
                ))
            else:
                await ctx.reply(embed=Embed(ctx=ctx,
                                            title="Hentai",
                                            description=f"Category must be one of this list: \n```" + '\n'.join(hentai.possible) + "```"))
