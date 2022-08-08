from modules.OnMessageEventInfo import OnMessageEventInfo
from utils.message_parser import *


class ParsePing:
    def __init__(self, ping: str):
        self.id = int(ping[2:-1])

    @staticmethod
    async def GetFirstMention(ctx: OnMessageEventInfo) -> discord.Member:
        return await ctx.message.guild.fetch_member(ParsePing(MessageParser(ctx).parsedContent[0]).id)
