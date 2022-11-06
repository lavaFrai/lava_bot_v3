import discord
import psutil
import platform
import random
import asyncio

from modules.Module import *
from utils.embed import *
from utils.ping_parser import *

import sys
import math

from utils.safeEvaluator import SafeEvaluator


def powTmp(a, b):
    if (-32569 <= a <= 32569) and (-32569 <= b <= 32569):
        return a ** b
    else:
        raise Exception("Для pow естановлены ограничения - 32569")


def factTmp(a):
    if -32569 <= a <= 32569:
        return math.factorial(a)
    else:
        raise Exception("Для fact естановлены ограничения - 32569")


def rangeTmp(a, b=None, c=None):
    if (-32569 <= a <= 32569) and (-32569 <= b <= 32569) and (-32569 <= c <= 32569):
        if b is None:
            return range(a)
        if c is None:
            return range(a, b)
        return range(a, b, c)
    else:
        raise Exception("Для range естановлены ограничения - 32569")


def sumTmp(a):
    if len(a) < 32569:
        if max(a) < 32569:
            return sum(a)
        else:
            raise Exception("Для sum естановлены ограничения максимума - 32569")
    else:
        raise Exception("Для sum естановлены ограничения длинны - 32569")


class Calc(Module):
    def __init__(self):
        super().__init__("calc",
                         Module.MODULE_CATEGORY_FUN,
                         description="Calculate math expressions.",
                         examples="<expressions>")

    async def onFinishListener(self, safeEval: SafeEvaluator, ctx: OnMessageEventInfo, message: discord.Message):
        if safeEval.error:
            await message.edit(embed=Embed(
                ctx=ctx,
                error=True,
                title="Вычисление выражения",
                description=f"Выражение: `{safeEval.expression}`\n"
                            f"Ошибка: `{safeEval.error}`"
            ))
        else:
            if len(f"{safeEval.result}") > 1024:
                await message.edit(embed=Embed(
                    ctx=ctx,
                    error=True,
                    title="Вычисление выражения",
                    description=f"Выражение: `{safeEval.expression}`\n"
                                f"Ошибка: `Результат слишком длинный`"
                ))
            else:
                await message.edit(embed=Embed(
                    ctx=ctx,
                    title="Вычисление выражения",
                    description=f"Выражение: `{safeEval.expression}`\n"
                                f"Результат: `{safeEval.result}`"
                ))

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        expression = ctx.server_config.GetRealText(ctx.message).strip()

        if len(expression) > 1024:
            await ctx.message.channel.send(embed=Embed(
                ctx=ctx,
                error=True,
                title="Вычисление выражения",
                description=f"Ошибка: `Выражение слишком длинное`"
            ))
            return

        message = await ctx.message.channel.send(embed=Embed(
            ctx=ctx,
            title="Вычисление выражения...",
            description=f"Выражение: `{expression}`\n"
                        f"Результат: `<in queue>`"
        ))

        safeEval = SafeEvaluator(expression)
        safeEval.addAsyncOnFinishListener(self.onFinishListener, args=(ctx, message))
        safeEval.start()
