import discord
import psutil
import platform
import random

import requests

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *
import openai

import sys
from utils.middleware.backdoorMiddleware import *


class Dalle2(Module):
    def __init__(self):
        super().__init__("dalle2",
                         Module.MODULE_CATEGORY_UTILITY,
                         description="Generating image by your prompt.",
                         aliases=["dalle"])

    def get_answer(self, prompt, api_key):
        openai.api_key = api_key
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
        )

        return response["data"][0]["url"]

    @onlyBackdoorMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        api_key = ctx.bot_config["openai_token"]
        prompt = ctx.server_config.GetRealText(ctx.message).strip()
        answer = self.get_answer(prompt, api_key)

        await ctx.message.reply(content=answer)

        # await ctx.message.reply(embed=Embed(ctx=ctx,
        #                                     title="ChatGPT",
        #                                     description="```\n" + answer + "```"))
