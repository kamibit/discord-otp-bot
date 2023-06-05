from asyncio import run

import discord
from discord.ext import commands

from data.config import TOKEN

BOT = commands.Bot(command_prefix=".", intents=discord.Intents.all())
COGS = ["cogs.cmds", "cogs.events"]

if __name__ == "__main__":

    async def start():
        print("starting...")
        [await BOT.load_extension(cog) for cog in COGS]

    run(start())
    BOT.run(TOKEN)
