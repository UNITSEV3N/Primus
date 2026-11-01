
import os
import discord
import traceback
from discord.ext import commands

from bot.core.service.settings import Settings

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!!", intents=discord.Intents.all(), case_insensitive=True)
        self.DEBUG = os.getenv("DEBUG", "false").lower() in ("1", "true")
        self.DEV_GUILD = discord.Object(str(os.getenv("GUILD_ID")))

        self.settings = Settings()

        if self.DEBUG:
            print(f"DEBUG MODE: {self.DEBUG}")

    async def load_cogs(self):
        cogs = self.settings.get_cogs()
        for cog in cogs:
            try:
                if cog == "debugger" and self.DEBUG is False:
                    continue

                await self.load_extension(f"bot.cogs.{cog}")
            except Exception as error:
                print(f"Failed to load {cog}: {error}: {traceback.print_exc()}")

    async def reload_cogs(self, reload_commands: bool = False):
        reloaded_cogs = []
        try:
            # Reload all currently selected/active cogs
            for i, extension in enumerate(list(self.extensions.keys())):
                await self.reload_extension(extension)
                reloaded_cogs.append(f"{i + 1}. {extension.removeprefix("bot.cogs.")}")

            # Reload/Refresh commands after all cogs have been updated
            # Only should ever reload commands in debug mode (for now)
            if reload_commands and self.DEBUG:
                await self.load_commands()

            return reloaded_cogs

        except Exception as error:
            print(f"Failed to reload cogs: {error}")
            return None

    async def load_commands(self):
        try:
            if self.DEBUG and self.DEV_GUILD:
                self.tree.clear_commands(guild=self.DEV_GUILD)
                self.tree.copy_global_to(guild=self.DEV_GUILD)
                synced = await self.tree.sync(guild=self.DEV_GUILD)

                print(f"\nSynced: {len(synced)} commands")
                for command in synced:
                    print(f"  > {command}")

            else:
                synced = await self.tree.sync()

                print(f"\nSynced: {len(synced)} commands")
                for command in synced:
                    print(f"  > {command}")

        except Exception as error:
            print(f"Failed to sync commands: {error}")

    async def update_presence(self):
        status_map = \
        {
            'online':       discord.Status.online,
            'offline':      discord.Status.offline,
            'idle':         discord.Status.idle,
            'dnd':          discord.Status.dnd,
            'invisible':    discord.Status.invisible
        }

        custom_activity = discord.CustomActivity(self.settings.get_configuration("activity"))
        custom_status = status_map.get(self.settings.get_configuration("status").lower(), status_map.get("idle"))

        await self.change_presence(activity=custom_activity, status=custom_status)

    async def setup_hook(self):
        await super().setup_hook()

        self.settings.initialize()
        await self.load_cogs()
        await self.load_commands()

    async def on_ready(self):
        await self.update_presence()
        print(f"\n{self.user.name} has connected to Discord!")