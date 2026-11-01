
import discord, datetime
from discord import app_commands
from discord.ext import commands

class Debugger:
    def __init__(self, client):
        super().__init__(client)

    @commands.is_owner()
    @app_commands.command(name="shutdown", description=f"Shutdown the bot")
    async def shutdown(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"Shutting down...", ephemeral=True)
        await self.client.close()

    @commands.is_owner()
    @app_commands.command(name="ping", description=f"Show the latency of the bot.")
    async def ping(self, ctx: discord.Interaction):
        await ctx.response.send_message(f"Pong! {round(self.client.latency * 1000)} ms", ephemeral=True)

    @commands.is_owner()
    @app_commands.command(name="reload", description=f"Reload all currently active cogs, and reload commands to current server.")
    async def reload(self, ctx: discord.Interaction, reload_commands: bool = None):
        try:
            await ctx.response.defer(ephemeral=True)

            success = await self.client.reload_cogs(reload_commands=reload_commands)
            if success is None:
                return await ctx.followup.send("Failed to reload cogs.", ephemeral=True)

            await ctx.followup.send(f"Reloaded the following extensions: \n```\n{'''\n'''.join(success)}\n```\n", ephemeral=True)
        except Exception as error:
            await ctx.response.send_message(f"{error}", ephemeral=True)

    @commands.is_owner()
    @app_commands.command(name="nuke_channel", description=f"Nuke all messages in current channel")
    async def nuke_channel(self, ctx: discord.Interaction):
        if not ctx.channel.permissions_for(ctx.guild.me).manage_messages:
            await ctx.response.send_message("Missing 'Manage Messages' permission.", ephemeral=True)

        await ctx.response.defer(ephemeral=True)
        total_deleted_messages = 0

        while True:
            try:
                deleted = await ctx.channel.purge(limit=1000)
                if not deleted:
                    break

                total_deleted_messages += len(deleted)
                await discord.utils.sleep_until(discord.utils.utcnow() + datetime.timedelta(seconds=1.0))

            except discord.HTTPException as e:
                await ctx.followup.send(f"Stopped early: {e}", ephemeral=True)
                break

        if total_deleted_messages == 0:
            await ctx.followup.send("No messages were deleted.", ephemeral=True)
        else:
            await ctx.followup.send(f"Deleted **{total_deleted_messages}** messages.", ephemeral=True)

async def setup(client: commands.Bot):
    await client.add_cog(Debugger(client))
