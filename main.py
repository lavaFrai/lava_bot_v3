# https://discord.com/oauth2/authorize?client_id=811539043778297857&scope=bot&permissions=8
import json
from utils.logger import *
import discord
from modules.ModuleManager import *


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

        # creating discord client
        self.logger.Log("Creating discord.client object")
        self.client = discord.Client(self_bot=True, intents=discord.Intents(messages=True, guilds=True, reactions=True))

        self.logger.Log("Registering bot events")
        self.client.event(self.on_ready)
        self.client.event(self.on_error)
        self.client.event(self.on_message)

        self.logger.Log("Registering bot modules")
        self.modules = ModuleManager()

        self.logger.Log("Initializing finished")
        self.status = self.LOAD_STATUS_SUCCESS

    def SelfCheck(self) -> bool:
        return True

    async def on_error(self, e):
        self.logger.Warning(f"In runtime detected error: {e}")

    async def on_ready(self):
        self.logger.Log(f"Login successfully as {self.client.user.name}#{self.client.user.discriminator}")

    async def on_message(self, ctx: discord.Message):
        self.logger.Debug(f"Received message from server {ctx.guild.id} by user {ctx.author.id} content: {ctx.content}")
        module = self.modules.getModule(ctx.content)
        if module is not None:
            await module.on_message(ctx)

    def Run(self):
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
