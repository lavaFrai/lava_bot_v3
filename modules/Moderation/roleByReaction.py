import datetime

from modules.Module import *
from utils.embed import Embed
from utils.middleware.sudoMiddleware import *
from utils.event.OnReactionAddEventInfo import OnReactionAddEventInfo
from utils.event.OnReactionRemoveEventInfo import OnReactionRemoveEventInfo


class RoleByReaction(Module):
    def __init__(self):
        super().__init__("reactionrole", Module.MODULE_CATEGORY_MODERATION,
                         aliases=["rr"],
                         description="Registrate new role by reaction",
                         examples="<role_ping>")

    @onlySudoMiddleware
    async def on_message(self, ctx: OnMessageEventInfo):
        super().on_message(ctx)

        if len(ctx.message.role_mentions) == 0:
            await TypicalAnswers.InvalidUsage(ctx.module.title, ctx)
            return

        role = ctx.message.role_mentions[0]

        message = await ctx.message.channel.send(embed=Embed(
            ctx=ctx,
            title=f"Role by reaction",
            description=f"Started registration of {role.mention} by reaction \n"
                        f"Please, react this message with emoji you want to use"
        ))

        dtime: datetime.datetime = message.created_at
        utime = time.mktime(dtime.timetuple())
        self.cache[message.id] = {"role": role.id, "emoji": None, "author": ctx.message.author.id, "created_at": utime}

    async def on_reaction_add(self, ctx: OnReactionAddEventInfo):
        super().load_cache(ctx)

        if str(ctx.reaction.message_id) not in self.cache:
            return

        guild = ctx.guild
        message = await guild.get_channel(ctx.reaction.channel_id).fetch_message(ctx.reaction.message_id)
        ctx.message = message
        member: discord.Member = await guild.fetch_member(ctx.reaction.user_id)

        if self.cache[str(ctx.reaction.message_id)]["emoji"] is None and ctx.reaction.user_id == self.cache[str(ctx.reaction.message_id)]["author"]:
            await message.add_reaction(ctx.reaction.emoji)
            reaction = ctx.reaction.emoji.name
            print(reaction)
            self.cache[str(ctx.reaction.message_id)]["emoji"] = reaction
            await message.edit(embed=Embed(
                ctx=ctx,
                title=f"Role by reaction",
                description=f"Reaction: {ctx.reaction.emoji} \n"
                            f"Role: {ctx.guild.get_role(self.cache[str(ctx.reaction.message_id)]['role']).mention}"
            ))

            while self.cache[str(ctx.reaction.message_id)]["emoji"] != reaction:
                self.cache[str(ctx.reaction.message_id)]["emoji"] = reaction

            super().save_cache(ctx)

        if self.cache[str(ctx.reaction.message_id)]["emoji"] is not None:
            if ctx.reaction.emoji.name == self.cache[str(ctx.reaction.message_id)]["emoji"]:
                try:
                    await member.add_roles(guild.get_role(self.cache[str(ctx.reaction.message_id)]["role"]))
                except discord.Forbidden:
                    await message.edit(embed=Embed(
                        ctx=ctx,
                        error=True,
                        title=f"Role by reaction",
                        description=f"I don't have permissions to edit role {ctx.guild.get_role(self.cache[str(ctx.reaction.message_id)]['role']).mention}"
                    ))
                    self.cache.pop(str(ctx.message.message_id))
                    super().save_cache(ctx)
                    return

    async def on_reaction_remove(self, ctx: OnReactionRemoveEventInfo):
        super().load_cache(ctx)

        if str(ctx.reaction.message_id) not in self.cache:
            return

        guild = ctx.guild
        message = await guild.get_channel(ctx.reaction.channel_id).fetch_message(ctx.reaction.message_id)
        ctx.message = message
        member: discord.Member = await guild.fetch_member(ctx.reaction.user_id)

        if self.cache[str(ctx.reaction.message_id)]["emoji"] is not None:
            if ctx.reaction.emoji.name == self.cache[str(ctx.reaction.message_id)]["emoji"]:
                try:
                    await member.remove_roles(guild.get_role(self.cache[str(ctx.reaction.message_id)]["role"]))
                except discord.Forbidden:
                    await message.edit(embed=Embed(
                        ctx=ctx,
                        error=True,
                        title=f"Role by reaction",
                        description=f"I don't have permissions to edit role {ctx.guild.get_role(self.cache[str(ctx.reaction.message_id)]['role']).mention}"
                    ))
                    self.cache.pop(str(ctx.message.message_id))
                    super().save_cache(ctx)
                    return

        super().save_cache(ctx)

    async def on_message_delete(self, ctx: OnMessageEventInfo):
        super().load_cache(ctx)

        if str(ctx.message.message_id) not in self.cache:
            return

        self.cache.pop(str(ctx.message.message_id))

        super().save_cache(ctx)
