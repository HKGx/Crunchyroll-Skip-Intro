from typing import Optional, Dict, Union

import discord
from discord.ext.commands import Cog, Bot, Context, group, check

import db


def has_botrole(role):

    def predicate(ctx):
        with db.db_session:
            user: db.BotRoles = db.BotRoles.get(id=ctx.author.id.__str__())
            return user.role & role

    return predicate


class CrunchyCog(Cog):
    _bot: Bot

    @group()
    async def episode(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            embed: discord.Embed = discord.Embed()
            embed.title = "No subcommand"
            embed.description = "Invoke me with subcommands:\n" \
                                "```\n" \
                                "get    — gets episode info\n" \
                                "add    — adds episode info\n" \
                                "addp   — adds episode info based on parameters\n" \
                                "update — updates episode info (*not implemented*)\n" \
                                "remove — removes episode (*not implemented*)\n" \
                                "```"
            await ctx.send(embed=embed)

    @episode.command("get")
    async def get(self, ctx: Context, ep_id: int):
        with db.db_session:
            episode = db.Episode.get(id=ep_id)
        embed: discord.Embed = discord.Embed()
        if not episode:
            embed.title = f"Episode {ep_id} not found!"
            embed.description = "Message us to add it!"
        else:
            embed.title = episode.full_episode_name
            embed.add_field(name="id", value=episode.id)
            embed.add_field(name="intro end", value=episode.intro_end)
        await ctx.send(embed=embed)

    @episode.command("addp")
    @check(has_botrole(db.ROLE_ADD))
    async def add_by_props(self, ctx: Context,
                           ep_id: int,
                           intro_end: float,
                           show: Optional[str],
                           name: Optional[str],
                           season: Optional[str]):
        ctx.bot: Bot
        with db.db_session:
            db.Episode(id=ep_id,
                       intro_end=intro_end,
                       show=show,
                       name=name,
                       season=season)

    @episode.command("add")
    @check(has_botrole(db.ROLE_ADD))
    async def add(self, ctx: Context):
        ctx.bot: Bot
        embed: discord.Embed = discord.Embed()

        def message_pred(m: discord.Message):
            return m.author == ctx.author and m.channel == ctx.channel

        def parse(fun, value):
            try:
                return fun(value)
            except ValueError:
                return None
        # key: type, needed
        mock_episode: Dict[Union[type, bool]] = {
            "id": (int, True),
            "intro_end": (int, True),
            "name": (str, False),
            "show": (str, False),
            "season": (str, False),
        }
        for x, y in mock_episode.items():
            print(x, y)
            await ctx.send(f"What's the {x}?")
            msg: discord.Message = await ctx.bot.wait_for("message", check=message_pred, timeout=30.0)
            parsed = parse(y[0], msg.content)
            if not parsed and y[1]:
                embed.title = "Oh crap!"
                embed.description = f"I couldn't parse {x}."
                await ctx.send(embed=embed)
            mock_episode[x] = parsed
        for x, y in mock_episode.items():
            if y is tuple:
                mock_episode[x] = None
        with db.db_session:
            db.Episode(**mock_episode)

    def __init__(self, bot: Bot):
        self._bot = bot


def setup(bot: Bot):
    bot.add_cog(CrunchyCog(bot))
