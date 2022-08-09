import discord
import psutil
import platform

from modules.Module import *
from utils.embed import *

import sys


class HostInfo(Module):
    def __init__(self):
        super().__init__("info", Module.MODULE_CATEGORY_INFORMATION)

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        ram_info = psutil.virtual_memory()
        uptime = time.time() - psutil.boot_time()

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title="Information about bot",
            description=f"📟 **Bot:**\n"
                        f"The **{ctx.client.user.name}#{ctx.client.user.discriminator}** bot\n"
                        f"Based on **lava.discord_bot_framework_v3**\n"
                        f"Interpreter version:\t  **Python {sys.version_info[0]}.{sys.version_info[1]}**\n"
                        f"Discord.py version:\t  **{discord.__version__}**\n"
                        f"Bot version:\t\t  **{ctx.bot_config['version']}**\n"
                        f"Bot is member on **{len(ctx.client.guilds)}** servers\n"
                        f"\n🌐 **Hosting:**\n"
                        f"RAM:\t  **{round(ram_info.used / 1024 / 1024 / 1024, 1)}G/{round(ram_info.total / 1024 / 1024 / 1024, 1)}G**\n"
                        f"CPU usage:\t  **{psutil.cpu_percent()}%**\n"
                        f"Operating system:\t  **{platform.system()} {platform.release()}**\n"
                        f"Database type:\t  **{ctx.bot_config['database_type']}**\n"
                        f"Uptime:\t  **{int(uptime // 60 // 60)} hours {int(uptime // 60 % 60)} minutes {int(uptime % 60)} seconds**\n"
                        f"Ping:\t  **{int(ctx.client.latency * 1000)}ms**\n\n"
                        f"You can invite the bot to your server and use for free\nInvite link: [* click *](https://discord.com/oauth2/authorize?client_id={ctx.bot_config['client_id']}&scope=bot&permissions=8)\n\n"
                        f"Developer:\t  [**lava_frai#0498**](https://discordapp.com/users/677933625802489889/)\n"
                        f"(c)lava_frai 2021-{time.strftime('%Y')}",
        ))
