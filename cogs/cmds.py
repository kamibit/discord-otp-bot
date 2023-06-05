from discord import Interaction, errors, app_commands, Embed, Color
from discord.ext import commands
from data.config import COLOR_CODE
from files.methods import (
    create_user,
    delete_user,
    get_user,
    is_e164_format,
    generate_otp,
    send_sms,
)
from files.views import VerifyCode

COLOR = Color.from_str(COLOR_CODE)


class Commands(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @app_commands.command(name="delete", description="Deletes User Account")
    async def delete(self, ctx: Interaction) -> None:
        try:
            await ctx.response.defer(ephemeral=True)
            delete_user(ctx.user.id)
            await ctx.followup.send(
                "Your account and asociated data is deleted from the DB", ephemeral=True
            )
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.command(name="info", description="Shows User Info")
    async def info(self, ctx: Interaction) -> None:
        try:
            await ctx.response.defer(ephemeral=True)
            data = get_user(ctx.user.id)
            if data is None:
                return await ctx.followup.send(
                    "Error: You dont have anything in the DB.", ephemeral=True
                )
            embed = Embed(title=ctx.user.name, description=None, color=COLOR)
            embed.add_field(name="Number", value=data[1], inline=True)
            embed.add_field(name="Verified", value=data[4], inline=True)
            embed.set_thumbnail(url=ctx.user.avatar.url)
            await ctx.followup.send(embed=embed)
        except Exception as err:
            await ctx.followup.send(err)

    @app_commands.checks.cooldown(1, 300, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="verify", description="Sends OTP to Provided Number")
    async def verify(self, ctx: Interaction, number: str) -> None:
        try:
            await ctx.response.defer(ephemeral=True)
            data = get_user(ctx.user.id)
            try:
                if data[4] == 1:
                    return await ctx.followup.send(
                        "Error: You are already verified, no need to use that again.",
                        ephemeral=True,
                    )
            except TypeError:
                pass
            if not is_e164_format(number):
                return await ctx.followup.send(
                    "Error: Please enter the number in E.164 format, for example +12345678910.",
                    ephemeral=True,
                )
            otp = generate_otp()
            create_user(ctx.user.id, number, otp)
            response = await send_sms(number, f"Your OTP code is: {otp}.")
            # print(otp)
            if response == "failed" or response == "undelivered":
                return await ctx.followup.send(
                    "Error: Unknow error occured, please try again later.",
                    ephemeral=True,
                )
            view = VerifyCode(timeout=60)
            await ctx.followup.send(
                f"Your OTP code sent to {number}.", view=view, ephemeral=True
            )
        except Exception as err:
            await ctx.followup.send(err)

    @verify.error
    async def verify_error(self, ctx: Interaction, error):
        try:
            if isinstance(error, app_commands.CommandOnCooldown):
                seconds = str(error.retry_after).split(".")[0]
                await ctx.response.send_message(
                    f"Error: You must wait atleast 5 minutes before generating OTP again. Try again in {seconds} seconds."
                )
        except errors.NotFound:
            pass
        except Exception as err:
            await ctx.followup.send(err)


async def setup(bot):
    await bot.add_cog(Commands(bot))
