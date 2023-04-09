from modules.Module import *
from utils.embed import *


class GuildInfo(Module):
    def __init__(self):
        super().__init__("server", Module.MODULE_CATEGORY_INFORMATION,
                         description="Get information about the server")

    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        owner = await ctx.message.guild.fetch_member(ctx.message.guild.owner_id)
        created_at = time.gmtime(time.mktime(ctx.message.guild.created_at.timetuple()))

        await ctx.message.reply(embed=Embed(
            ctx=ctx,
            title=f"Information about **{ctx.message.guild.name}**:",
            description=f"\n\nID: **{ctx.message.guild.id}**"
                        f"\nOwner: **{owner.mention}**"
                        f"\nPrefix: **{ctx.server_config.prefix}**"
                        f"\n\nMembers count: **{ctx.message.guild.member_count}**"
                        f"\n\nText channels: **{len(ctx.message.guild.text_channels)}**"
                        f"\nVoice channels: **{len(ctx.message.guild.voice_channels)}**"
                        f"\n\nVerification level: **{str(ctx.message.guild.verification_level).capitalize()}**"
                        f"\n\nCreated at: **{time.strftime('%d %b %Y', created_at)}**"
        ).set_image(url=ctx.message.guild.icon.url))
