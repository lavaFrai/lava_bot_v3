from utils.event import OnReactionAddEventInfo, OnReadyEventInfo
from utils.event.OnMessageRemoveEventInfo import OnMessageRemoveEventInfo
from utils.logger import *
from utils.message_parser import *
from utils.server_configuration import *
from utils.event.OnMessageEventInfo import *
from utils.event.OnReadyEventInfo import *
from utils.b64 import *


class Module:
    MODULE_CATEGORY_INFORMATION = "Information"
    MODULE_CATEGORY_MODERATION = "Moderation"
    MODULE_CATEGORY_ADMINISTRATION = "Administration"
    MODULE_CATEGORY_NSFW = "NSFW"
    MODULE_CATEGORY_FUN = "Fun"
    MODULE_CATEGORY_UTILITY = "Utility"

    def __init__(self,
                 name: str,
                 category: str,
                 description: str = None,
                 examples: list = None,
                 aliases=None,
                 title: str = None,
                 visible: bool = True):
        self.logger = Logger(Logger.LOG_LEVEL_DEBUG)
        self.name = name
        self.category = category
        self.description = description
        self.examples: str = examples
        self.parse: MessageParser = None
        self.cache: dict = {}
        self.visible = visible
        self.moduleid = f"{b64toBytes(self.category)}:{b64toBytes(self.name)}"

        self.aliases = aliases
        if aliases is not None:
            self.aliases = list(map(lambda x: x.lower(), aliases))

        self.title = title
        if title is None:
            self.title = name.capitalize()

    def IsAliasFor(self, name: str) -> bool:
        if self.aliases is None:
            return name.lower() == self.name
        return name.lower() in self.aliases or name.lower() == self.name

    async def on_ready(self, ctx: OnReadyEventInfo):
        pass

    def on_message(self, ctx: OnMessageEventInfo):
        self.parse = MessageParser(ctx)
        self.load_cache(ctx)
        self.logger.Log(f"Handling command {ctx.message.content} by user {ctx.message.author.id} on server {ctx.message.guild.id}")

    async def on_message_delete(self, ctx: OnMessageRemoveEventInfo):
        pass

    async def on_reaction_add(self, ctx: OnReactionAddEventInfo):
        pass

    async def on_reaction_remove(self, ctx: OnReactionAddEventInfo):
        pass

    def load_cache(self, ctx: OnMessageEventInfo):
        temporary_data = ctx.database.get(f"SELECT value FROM cache WHERE moduleid='{self.moduleid}'")
        if len(temporary_data) == 0:
            ctx.database.send(f"INSERT INTO cache (moduleid, value) VALUES ('{self.moduleid}', '{b64toBytes(json.dumps(self.cache))}')")
            ctx.database.save()
        temporary_data = ctx.database.get(f"SELECT value FROM cache WHERE moduleid='{self.moduleid}'")
        self.cache = json.loads(b64fromBytes(temporary_data[0][0]))

    def save_cache(self, ctx: OnMessageEventInfo):
        ctx.database.send(f"UPDATE cache SET value='{b64toBytes(json.dumps(self.cache))}' WHERE moduleid='{self.moduleid}'")
        ctx.database.save()
