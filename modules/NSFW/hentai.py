import random

import discord
import hmtai

from modules.Module import *
from utils.server_configuration import *
from utils.typical_answers import *
from utils.ping_parser import *
from utils.hentai import *
from utils.embed import *
from utils.nsfwMiddleware import *


class Hentai(Module):
    def __init__(self):
        super().__init__("hentai", Module.MODULE_CATEGORY_NSFW,
                         aliases=["hent"],
                         description="Sends a picture with NSFW content",
                         examples="\n"
                                  "<tag>")

    @onlyNSFWMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        hentai = HentaiGenerator()

        if len(self.parse) == 0:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Hentai"
            ).set_image(
                url=hentai.GetRandomUrl()
            ))
        else:
            if self.parse.parsedContent[0] in hentai.possible:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    title="Hentai",
                    description=self.parse.parsedContent[0]
                ).set_image(
                    url=hentai.GetRandomUrl(self.parse.parsedContent[0])
                ))
            else:
                await ctx.message.reply(embed=Embed(ctx=ctx,
                                                    title="Hentai",
                                                    description=f"Category must be one of this list: \n```" + '\n'.join(
                                                        hentai.possible) + "```"))
