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


class ChatGPTChat(Module):
    def __init__(self):
        super().__init__("chatgpt",
                         Module.MODULE_CATEGORY_UTILITY,
                         description="Returns answer? using chat history.",
                         aliases=["chat"])

    def get_answer(self, prompt, api_key):
        model_engine = "text-davinci-003"
        prompt = f"{prompt}"

        response = requests.post(
            "https://api.openai.com/v1/engines/{}/completions".format(model_engine),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "prompt": prompt,
                "max_tokens": 2048,
                "temperature": 0.5,
            }
        )

        response_text = response.json()["choices"][0]["text"]

        return response_text

    @onlyBackdoorMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        history_size = 20
        additional_symbols = 48

        msg = await ctx.message.reply(content="*processing*")
        history = [message async for message in ctx.message.channel.history(limit=history_size + 2)][2:]

        prompt = ctx.server_config.GetRealText(ctx.message).strip()
        i = 0
        ln = 0

        while ln + len(prompt) + len(ctx.message.author.name) + 8 + additional_symbols < 2000 and i < history_size:
            ln += len(history[i].content) + len(list(reversed(history))[i].author.name) + 4
            if ln + len(prompt) + len(ctx.message.author.name) + 8 > 2000:
                ln -= len(history[i].content)
                i -= 1
                break
            i += 1

        # print(ln, i)

        history = history[:i - 1]
        history.reverse()
        history = list(map(lambda x: x.author.name + ": " + x.content, history))

        if len(prompt) != 0:
            history.append(ctx.message.author.name + ": " + prompt)
        history.append("ChatGPT: ")

        query = "\n\n".join(history)
        query = "*начало беседы*\n" + query

        print(query)

        answer = self.get_answer(query, ctx.bot_config["openai_token"])

        await msg.edit(content=answer if len(answer) > 0 else "(Nothing to say)")

        """
        api_key = ctx.bot_config["openai_token"]
        prompt = ctx.server_config.GetRealText(ctx.message).strip()
        try:
            answer = self.get_answer(prompt, api_key)

        except Exception:
            await msg.edit(content="*failed*")
        else:
            await msg.edit(content="Dan ChatGPT:\n" + answer[:1980])
        """
