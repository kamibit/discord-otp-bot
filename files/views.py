import discord
from data.config import VERIFIED_ROLE_ID

from files.methods import get_user, update_verify


class VerifyCode(discord.ui.View):
    @discord.ui.button(label="Continue", style=discord.ButtonStyle.primary)
    async def submit(self, ctx: discord.Interaction, button: discord.ui.Button):
        data = get_user(ctx.user.id)
        if data[4] == 1:
            return await ctx.response.send_message(
                "Err: You are already verified, no need to use that again."
            )
        await ctx.response.send_modal(VerifyCodeSubmit())


class VerifyCodeSubmit(discord.ui.Modal, title="Verification"):
    otp_field = discord.ui.TextInput(
        label="Enter OTP code sent to your phone number:", style=discord.TextStyle.short
    )

    async def on_submit(self, ctx: discord.Interaction):
        await ctx.response.defer(ephemeral=True)
        data = get_user(ctx.user.id)
        if not str(self.otp_field) == str(data[2]):
            return await ctx.followup.send(
                "Err: Account verificaton failed, please check OTP and try again.",
                ephemeral=True,
            )
        update_verify(ctx.user.id, 1)
        ROLE = ctx.guild.get_role(VERIFIED_ROLE_ID)
        await ctx.user.add_roles(ROLE)
        await ctx.followup.send(
            f"✅ Verification Successful. You have been given {ROLE.mention}, enjoy.",
            ephemeral=True,
        )
