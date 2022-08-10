from utils.event.OnMessageEventInfo import OnMessageEventInfo
from utils.embed import Embed
from functools import wraps


def onlyNSFWMiddleware(func):
    @wraps(func)
    async def wrapper(self, ctx: OnMessageEventInfo):
        if ctx.message.channel.is_nsfw():
            await func(self, ctx)
        else:
            await ctx.message.reply(embed=Embed(ctx=ctx,
                                                error=True,
                                                title=ctx.module.title,
                                                description=f"Sorry, i can't send that in this channel, it is not NSFW channel"))
    return wrapper
