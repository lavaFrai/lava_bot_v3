from utils.event.OnMessageEventInfo import OnMessageEventInfo
from utils.typical_answers import TypicalAnswers
from functools import wraps


def onlyBackdoorMiddleware(func):
    @wraps(func)
    async def wrapper(self, ctx: OnMessageEventInfo):
        if ctx.message.author.id in ctx.bot_config["backdoor_admins"]:
            await func(self, ctx)
        else:
            pass
    return wrapper
