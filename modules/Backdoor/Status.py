from modules.Module import *
from utils.embed import *

import sys

from utils.middleware.backdoorMiddleware import onlyBackdoorMiddleware
from utils.typical_answers import TypicalAnswers


class Status(Module):
    def __init__(self):
        super().__init__("status",
                         Module.MODULE_CATEGORY_ADMINISTRATION,
                         description="Set new bot status",
                         examples="<playing / watching / streaming / listening> <status>",
                         visible=False)

    async def on_ready(self, ctx: OnReadyEventInfo):
        super().load_cache(ctx)

        activities = {
            "PLAYING": discord.ActivityType.playing,
            "STREAMING": discord.ActivityType.streaming,
            "WATCHING": discord.ActivityType.watching,
            "LISTENING": discord.ActivityType.listening
        }

        if self.cache.get("enabled") is None:
            self.cache["enabled"] = True
        if self.cache.get("text") is None:
            self.cache["text"] = "No status set"
        if self.cache.get("type") is None:
            self.cache["type"] = "PLAYING"

        if self.cache["enabled"]:
            await ctx.client.change_presence(activity=discord.Activity(type=activities[self.cache["type"]],
                                                                       name=self.cache["text"]))

        super().save_cache(ctx)

    @onlyBackdoorMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        if len(self.parse.parsedContent) < 2:
            await TypicalAnswers.InvalidUsage(ctx.module.title,
                                              ctx)
            return

        self.cache["enabled"] = True
        if self.parse.parsedContentLower[0] == "listening":
            self.cache["type"] = "LISTENING"
        elif self.parse.parsedContentLower[0] == "watching":
            self.cache["type"] = "WATCHING"
        elif self.parse.parsedContentLower[0] == "streaming":
            self.cache["type"] = "STREAMING"
        elif self.parse.parsedContentLower[0] == "playing":
            self.cache["type"] = "PLAYING"
        else:
            await TypicalAnswers.InvalidUsage(ctx.module.title,
                                              ctx)
            return

        self.cache["text"] = " ".join(self.parse.parsedContent[1:])

        super().save_cache(ctx)

        await self.on_ready(ctx)

        await ctx.message.reply(embed=Embed(ctx=ctx,
                                            title="Status set",
                                            description=f"Status set to \n```\n**{self.cache['type'].upper()}** {self.cache['text']}\n```"))
