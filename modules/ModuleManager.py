import discord

from modules.Backdoor.ServersList import ServersList
from modules.Backdoor.Status import Status
from modules.Information.debuginfo import DebugInfo
from modules.Information.guildinfo import GuildInfo
from modules.Information.hostinfo import HostInfo
from modules.ServerControls.prefix import SetPrefix
from modules.ServerControls.addAdmin import AdminControls
from modules.Moderation.Kick import *
from modules.Moderation.Ban import *
from modules.Moderation.roleByReaction import *
from modules.NSFW.hentai import *
from modules.Utilites.Avatar import *
from modules.Utilites.Random import *
from modules.Utilites.Calc import *
from modules.Fun.Coin import *
from modules.Fun.EightBall import *
from utils.server_configuration import *
from utils.embed import *


class ModuleManager:
    def __init__(self):
        self.Modules = list()
        self.Categories = set()

        # Administration
        self.Modules.append(AdminControls())
        self.Modules.append(SetPrefix())

        # Moderation
        self.Modules.append(KickMember())
        self.Modules.append(BanMember())
        self.Modules.append(RoleByReaction())
        # self.Modules.append(MuteMember())

        # Information
        # self.Modules.append(DebugInfo())
        self.Modules.append(HostInfo())
        self.Modules.append(GuildInfo())

        # NSFW
        self.Modules.append(Hentai())

        # Utils
        self.Modules.append(Avatar())
        self.Modules.append(Calc())
        self.Modules.append(Random())

        # Fun
        self.Modules.append(Coin())
        self.Modules.append(EightBall())

        # Backdoor
        self.Modules.append(Status())
        self.Modules.append(ServersList())

        for i in self.Modules:
            self.Categories.add(i.category)
        self.CategoriesLower = list(map(lambda x: x.lower(), self.Categories))

    def getModule(self, name: str):
        name = name.lower()
        for i in self.Modules:
            if i.IsAliasFor(name):
                return i
        return None

    async def on_help(self, ctx: OnMessageEventInfo):
        parse = MessageParser(ctx)

        if len(parse) == 0:
            description = f"You can also view each category in more detail by `{ctx.server_config.prefix}help <category name>`\n" \
                          f"**Don't use `<` and `>` symbols in command**\n"
            for category_name in self.Categories:
                description += f"\n**{category_name}**\n > "
                for module in filter(lambda x: x.category == category_name, self.Modules):
                    if module.visible:
                        description += f"`{ctx.server_config.prefix}{module.name}` "
            await ctx.message.reply(embed=Embed(
                ctx=ctx,
                title="Available commands:",
                description=description
            ))

        else:
            if parse[0].lower() not in self.CategoriesLower:
                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    error=True,
                    title="Available commands",
                    description=f"The `{parse[0].lower()}` category does not exist\n"
                                f"Maybe need to remove `<` and `>` symbols from category name"
                ))

            else:
                description = ""

                for module in filter(lambda x: x.category.lower() == parse[0].lower(), self.Modules):
                    if module.visible:
                        description += f"\n**{module.name.capitalize()}** \n"
                        if module.description is None:
                            description += f" > *Without description*\n"
                        else:
                            description += f" > {module.description} \n"

                        if module.examples is not None:
                            description += '```\n'
                            for example in module.examples.split('\n'):
                                description += f"{ctx.server_config.prefix}{module.name.lower()} {example}\n"
                            description += '\n```'

                await ctx.message.reply(embed=Embed(
                    ctx=ctx,
                    title=f"Available commands in `{parse[0].lower()}`:",
                    description=description
                ))
