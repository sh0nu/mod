from discord.ext.commands import Cog
from discord.ext.commands import command
from random import choice, randint
from discord import Member
from typing import Optional
from discord.errors import HTTPException
from discord.ext.commands import BadArgument
from aiohttp import request


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello', 'Hi', 'Hey', 'Hiya'))} {ctx.author.mention}!")

    @command(name='dice', aliases=['roll'])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        if dice <= 25:
            rolls = [randint(1, value) for i in range(dice)]

            await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

        else:
            await ctx.send('You want to blow me up??')

    @command(name='slap', aliases=['hit'])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = 'no reason'):
        await ctx.send(f'{ctx.author.display_name} slapped {member.mention} for {reason}!')

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, BadArgument):
            await ctx.send('Can not find that member. Stop dreaming about fake friends.')

    @command(name='echo', aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('fun')
        print(' fun cog ready')


async def setup(bot):
    await bot.add_cog(Fun(bot))
