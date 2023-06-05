from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.bot.tree.sync()
            print(f"{self.bot.user.name} is online now.")
        except Exception as err:
            print(err)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            await ctx.send(error)
        except Exception as err:
            print(err)


async def setup(bot):
    await bot.add_cog(Events(bot))
