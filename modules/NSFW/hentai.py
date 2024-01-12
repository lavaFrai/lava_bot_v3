from rule34Py import rule34Py

from modules.Module import *
from utils.hentai import *
from utils.middleware.nsfwMiddleware import *


class Hentai(Module):
    def __init__(self):
        super().__init__("hentai", Module.MODULE_CATEGORY_NSFW,
                         aliases=["hent"],
                         description="Sends a picture with NSFW content",
                         examples="\n"
                                  "<tags>")

    @onlyNSFWMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        hentai = rule34Py()

        if len(self.parse) == 0:
            image = hentai.random_post()
            if isinstance(image, list):
                await ctx.message.reply(embed=Embed(ctx=ctx,
                                        title="Hentai",
                                        error=True,
                                        description=f"Not a single image was found for this tag. Try writing in English or using other tags"))
            else:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    url=f"https://rule34.xxx/index.php?page=post&s=view&id={image.id}",
                    title="Hentai"
                ).set_image(
                    url=image.image
                ))
        else:
            image = hentai.random_post(self.parse.parsedContent)
            if isinstance(image, list):
                await ctx.message.reply(embed=Embed(ctx=ctx,
                                        title="Hentai",
                                        error=True,
                                        description=f"Not a single image was found for this tag. Try writing in English or using other tags"))
            else:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    title="Hentai",
                    url=f"https://rule34.xxx/index.php?page=post&s=view&id={image.id}",
                    description=", ".join(self.parse.parsedContent)
                ).set_image(
                    url=image.image
                ))


"""
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
"""