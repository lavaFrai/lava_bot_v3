from utils.event.OnMessageEventInfo import OnMessageEventInfo
from utils.typical_answers import TypicalAnswers
from functools import wraps


def onlySudoMiddleware(func):
    @wraps(func)
    async def wrapper(self, ctx: OnMessageEventInfo):
        if ctx.server_config.IsUserAdmin(ctx.message.author.id) or ctx.message.author.guild_permissions.administrator:
            await func(self, ctx)
        else:
            await TypicalAnswers.NeedAdmin(ctx.module.title, ctx)
    return wrapper
