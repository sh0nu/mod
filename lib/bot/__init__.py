import asyncio
from datetime import datetime
from glob import glob
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed, Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import (
    CommandNotFound, BadArgument, MissingRequiredArgument, CommandOnCooldown)
from asyncio import sleep
from ..db import db
from discord import HTTPException, Forbidden

PREFIX = '+'
OWNER_IDS = [1038119543127683103]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f" {cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        self.ready = False
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            intents=intents)

        print(' setup complete')

    async def setup(self):
        for cog in COGS:
            await self.load_extension(f"lib.cogs.{cog}")
            print(f" {cog} cog loaded")

    def run(self, version):
        self.VERSION = version
        print(' running bot...')

        print(' running setup')

        asyncio.run(self.setup())

        print(' setup 2 complete')

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send('Remember to add here to the rules!')

    async def on_connect(self):
        print(' Bot has connected')

    async def on_disconnect(self):
        print(' bot disconnected')

    async def on_error(self, err, *args, **kwargs):
        if err == 'on_command_error':
            await args[0].send("Something went wrong, I am sorry that ShOnU is stupid")
        else:
            channel = self.get_channel(896878848807960646)
            await self.stdout.send(' an error occured')

        raise

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
            pass

        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send("You have to give me more info than that")

        # elif isinstance(exc.original, HTTPException):
            # await ctx.send('Unable to send message')

        elif isinstance(exc, CommandOnCooldown):
            await ctx.send(f'that command is on cooldown. Try again in {exc.retry_after:,.2f} seconds')

        elif hasattr(exc, 'original'):
            if isinstance(exc.original, Forbidden):
                await ctx.send("I do not have permission to do that")

        else:
            raise exc.original

    async def on_ready(self):
        if not self.ready:

            self.stdout = self.get_channel(896878848807960646)
            # self.scheduler.add_job(self.rules_reminder, CronTrigger(
            # day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()
            self.ready = True
            print(' bot ready')

            await self.stdout.send(' Now online!')

            # embed = Embed(title="now online!",
            #              description="shonu_but_smarter is now online", colour=0xFF0000, timestamp=datetime.utcnow())
            # fields = [('Name', 'Value', True), ("another field",
            #                                    "this field is next to the other one.", True),
            #         ('A non-inline field', 'this field will appear on its own row', False)]
            # for name, value, inline in fields:
            #    embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name='why do i program',
            #                 icon_url='https://tse1.mm.bing.net/th?id=OIP.Wytlw5AmN2HoCJ_kLGF1EgHaF7&pid=Api&rs=1&c=1&qlt=95&w=133&h=106')
            #embed.set_footer(text='This is a footer')
            # await channel.send(embed=embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

        else:
            print(' bot reconnected')

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)


print(' IS IT HERE!?')

bot = Bot()
