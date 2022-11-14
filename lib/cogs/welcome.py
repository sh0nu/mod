from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Forbidden
from ..db import db


class Welcome(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('welcome')
        print(' welcome cog ready')

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT INTO exp (UserID) VALUES (?)", member.id)
        await self.bot.get_channel(896875653645869066).send(f"welcome {member.mention}!")
        try:
            await member.send(f"Welcome to **{member.guild.name}**!")

        except Forbidden:
            pass

    @Cog.listener()
    async def on_member_remove(self, member):
        db.execute("EXECUTE FROM exp WHERE UserID = ?")


async def setup(bot):
    await bot.add_cog(Welcome(bot))
