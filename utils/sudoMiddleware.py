from modules.OnMessageEventInfo import OnMessageEventInfo
from utils.typical_answers import TypicalAnswers
from functools import wraps


def onlySudoMiddleware(func):
    @wraps(func)
    async def wrapper(self, ctx: OnMessageEventInfo):
        if ctx.server_config.IsUserAdmin(ctx.message.author.id):
            await func(self, ctx)
        else:
            await TypicalAnswers.NeedAdmin(ctx.module.title, ctx)
    return wrapper
