import json

from utils.event.OnMessageEventInfo import *


class Embed(discord.Embed):
    def __init__(self, ctx: OnMessageEventInfo, error: bool = False, **args):

        if ctx is not None:
            # self.set_author(name=ctx.author.display_name,
            #                 icon_url=ctx.author.avatar_url)
            self.set_footer(text=f"Executed for {ctx.message.author.display_name} | {ctx.client.user.name}",
                            icon_url=ctx.message.author.avatar.url)

        with open("config/colors.json", 'r') as f:
            colors = json.JSONDecoder().decode(f.read())

        if error:
            color = colors["error"]
        else:
            color = colors["success"]

        color = color.lstrip('#')
        color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

        super().__init__(**args,
                         colour=discord.Colour.from_rgb(color[0], color[1], color[2]))
