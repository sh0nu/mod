from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import discord
from discord.ext import commands
from discord import Embed
from datetime import datetime
from better_profanity import profanity


class Log(Cog):

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('log')

    @Cog.listener()
    async def on_message(self, message):

        embed = discord.Embed(
            title="Message sent", description=message.author,
            color=message.author.color,
            timestamp=datetime.now())
        embed.add_field(name="The message is:", value=message.content)
        embed.add_field(name=f"The channel is:",
                        value=message.channel.mention)

        self.channel = self.bot.get_channel(1041836411055263754)
        await self.channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        embed = discord.Embed(
            title="Message edited", description=before.author, color=before.author.color,
            timestamp=datetime.now())
        embed.add_field(name="The message was:", value=before.content)
        embed.add_field(name="The message is now:", value=after.content)
        self.channel = self.bot.get_channel(1041836411055263754)
        await self.channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = Embed(title="Message deletion",
                          description=f"Action by {message.author.display_name}.",
                          colour=message.author.colour,
                          timestamp=datetime.now())

            fields = [("Content", message.content, False)]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            self.channel = self.bot.get_channel(1041836411055263754)
            await self.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Log(bot))
