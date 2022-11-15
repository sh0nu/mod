from discord.ext.commands import Cog
from discord import Embed
from discord.ext.commands import command
from datetime import datetime


class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("log")

    @Cog.listener()
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            embed = Embed(title="Nickname change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            fields = [("Before", before.display_name, False),
                      ("After", after.display_name, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            self.channel = self.bot.get_channel(1041836411055263754)
            await self.channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            pass

    @Cog.listener()
    async def on_message_delete(self, before, after):
        if not after.author.bot:
            pass


async def setup(bot):
    await bot.add_cog(Log(bot))
