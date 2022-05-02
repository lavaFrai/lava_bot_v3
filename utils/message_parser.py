import discord


class MessageParser:
    def __init__(self, ctx: discord.Message):
        self.text = ctx.content
        self.ctx = ctx
