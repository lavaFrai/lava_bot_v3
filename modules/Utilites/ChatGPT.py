import discord
import psutil
import platform
import random

import requests

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys
from utils.middleware.backdoorMiddleware import *


class ChatGPT(Module):
    def __init__(self):
        super().__init__("gpt",
                         Module.MODULE_CATEGORY_UTILITY,
                         description="Returns answer to your ask.",
                         aliases=["chatgpt"])

    def get_answer(self, prompt, api_key):
        model_engine = "text-davinci-002"
        prompt = f"{prompt}"

        response = requests.post(
            "https://api.openai.com/v1/engines/{}/completions".format(model_engine),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "prompt": prompt,
                "max_tokens": 1024,
                "temperature": 0.5,
            }
        )

        response_text = response.json()["choices"][0]["text"]

        return response_text

    @onlyBackdoorMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        api_key = ctx.bot_config["openai_token"]
        prompt = ctx.server_config.GetRealText(ctx.message).strip()
        answer = self.get_answer(prompt, api_key)

        #answer.replace("<code>", "```\n")
        #answer.replace("</code>", "\n```")

        # await ctx.message.reply(content=answer)

        await ctx.message.reply(embed=Embed(ctx=ctx,
                                            title="ChatGPT",
                                            description="```\n" + answer + "```"))
