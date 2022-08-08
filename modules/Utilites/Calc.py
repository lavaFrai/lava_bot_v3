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
    allowed_functions = {
        "range": rangeTmp,
        "list": list,
        "set": set,
        "str": str,
        "int": int,
        "sin": lambda x: math.sin(math.radians(x)),
        "cos": lambda x: math.cos(math.radians(x)),
        "tan": lambda x: math.tan(math.radians(x)),
        "asin": lambda x: math.degrees(math.asin(x)),
        "acos": lambda x: math.degrees(math.acos(x)),
        "atan": lambda x: math.degrees(math.atan(x)),
        "hypotenuse": math.hypot,
        "pow": powTmp,
        "pi": math.pi,
        "e": math.e,
        "deg": math.degrees,
        "rad": math.radians,
        "abs": abs,
        "fact": factTmp,
        "sum": sumTmp,
        "log": math.log,
        "sqrt": math.sqrt,
        "gamma": math.gamma
    }

    def __init__(self):
        super().__init__("calc",
                         Module.MODULE_CATEGORY_FUN,
                         description="Calculate math expressions.",
                         examples="<expressions>")

    @staticmethod
    async def calculate(exp: str):
        result = eval(exp, {'__builtins__': Calc.allowed_functions})
        return result

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        expression = ctx.server_config.GetRealText(ctx.message)

        if expression.find("__") != -1:
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                error=True,
                title="Calc error",
                description=f"Security error: `Not a safe expression` \n"))
            return

        result = None

        try:
            result = await asyncio.wait_for(Calc.calculate(expression), timeout=5)
        except asyncio.TimeoutError:
            print("timed out")
            return

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title="Calc",
            description=f"{expression} = {result}"))

        pass
