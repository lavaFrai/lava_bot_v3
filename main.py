# https://discord.com/oauth2/authorize?client_id=811539043778297857&scope=bot&permissions=8
import json
from utils.logger import *
import discord
import os
from modules.ModuleManager import *
from utils.database import *
from utils.server_configuration import *


class LavaBot:
    LOAD_STATUS_FAIL = -1
    LOAD_STATUS_SUCCESS = 0

    def __init__(self, config_file="config/config.json"):
        self.logger = Logger(Logger.LOG_LEVEL_DEBUG)
        self.status = self.LOAD_STATUS_FAIL

        # loading bot configuration
        try:
            self.logger.Log("Loading configuration")
            with open(config_file, 'r') as f:
                self.config = json.JSONDecoder().decode(f.read())
        except FileNotFoundError:
            self.logger.Error("Failed to load config")
            return

        # creating discord client
        self.logger.Log("Creating discord.client object")
        self.client = discord.Client(self_bot=True, intents=discord.Intents(messages=True, guilds=True, reactions=True))

        self.logger.Log("Registering bot events")
        self.client.event(self.on_ready)
        # self.client.event(self.on_error)
        self.client.event(self.on_message)

        self.logger.Log("Registering bot modules")
        self.modules = ModuleManager()

        self.logger.Log("Initializing finished")
        self.database = None
        self.status = self.LOAD_STATUS_SUCCESS

    def SelfCheck(self) -> bool:
        if not os.path.exists("data"):
            os.mkdir("data")
            self.logger.Warning("Not found data catalog")
        if not os.path.exists("data\\" + self.config["default_database"]):
            open("data\\" + self.config["default_database"], 'w').close()
            self.logger.Warning("Not found database")
        self.logger.Log("Checking database tables")

        self.database = BotDatabase(self.config)
        self.database.send("""create table if not exists servers
                            (
                                id     TINYTEXT,
                                prefix TINYTEXT,
                                admin  TEXT
                            );""")
        self.database.save()

        return True

    async def on_error(self, event, *args, **kwargs):
        self.logger.Warning(f"In runtime detected error: {event}")

    async def on_ready(self):
        self.logger.Log(f"Login successfully as {self.client.user.name}#{self.client.user.discriminator}")

    async def on_message(self, ctx: discord.Message):
        server_config = ServerConfiguration(ctx, self.database, self.config)
        self.logger.Debug(f"Received message from server {ctx.guild.id} by user {ctx.author.id} content: {ctx.content}")

        if server_config.CheckForValidPrefix(ctx) and not ctx.author.bot:
            if server_config.GetCommandText(ctx) == "help":
                self.logger.Log(f"Handling help output for user {ctx.author.id} on server {ctx.guild.id}")
                context = OnMessageEventInfo(ctx, self.client, self.database, self.config, server_config, None)
                await self.modules.on_help(context)
            else:
                module = self.modules.getModule(server_config.GetCommandText(ctx))
                if module is not None:
                    context = OnMessageEventInfo(ctx, self.client, self.database, self.config, server_config, module)
                    await module.on_message(context)

    def Run(self):
        self.database = BotDatabase(self.config)
        try:
            self.client.run(self.config["token"])
        except BaseException:
            self.logger.Error("Failed to login by token")


bot = LavaBot()
if bot.status == LavaBot.LOAD_STATUS_FAIL:
    exit(-1)
if not bot.SelfCheck():
    exit(-2)
bot.Run()
