import asyncio
import os
import discord

from discord import app_commands
from discord.ext import commands

from bot import ASSET_ROOT
from bot.core.exception import MemberExists, AuthorizationError
from bot.core.service.access.member import Member
from bot.core.service.database import Database
from bot.util.discord import set_nickname
from bot.util.rolemanager import update_roles

class Ranker:
    def __init__(self, client):
        super().__init__(client)
        self._member_access = Member()

    # COMMANDS ---------------------------------------------------------------------------------------------------------

    @app_commands.command(name="screen", description=f"This is a description")
    async def _screen(self, ctx: discord.Interaction, member: str, name: str, platform: str):
        await ctx.response.defer(ephemeral=True)

        if not await self.has_authorisation(ctx):
            return None

        _member = ctx.guild.get_member(int(member))

        message = discord.Embed(
            title="SCREEN"
        )
        
        success = await asyncio.to_thread(self._member_access.add_member, _member.id, name, platform, "RECRUIT")
        if success:
            await set_nickname(_member, name)

            # If successful add some text to embed message
            message.add_field(name="", value=f'"{name}" was successfully screened.', inline=True)
            message.set_thumbnail(url=_member.avatar.url)

            # assign roles
            await update_roles(ctx, _member, [1525974580433518622])

            return await ctx.followup.send(embed=message, ephemeral=True)
        else:
            # Send failure message
            message.add_field(name="", value=f"Failed to add {_member.mention}", inline=True)
            return await ctx.followup.send(embed=message, ephemeral=True)

    @app_commands.command(name="enlist", description=f"This is a description")
    async def _enlist(self, ctx: discord.Interaction, member: str):
        await ctx.response.defer(ephemeral=True)

        if not await self.has_authorisation(ctx):
            return None
        
        Database.check()

        # _member = ctx.guild.get_member(int(member))

        message = discord.Embed(
            title="SCREEN"
        )
        message.add_field(name="", value="Database connection OK", inline=False)

        return await ctx.followup.send(embed=message, ephemeral=True)

    @app_commands.command(name="rename", description=f"This is a description")
    async def _rename(self, ctx: discord.Interaction, member: str, new_name: str):
        await ctx.response.defer(ephemeral=True)
        _member = ctx.guild.get_member(int(member))

        message = discord.Embed(
            title="SCREEN"
        )

        success = await asyncio.to_thread(self._member_access.update_name, _member.id, new_name)
        if success:
            await set_nickname(_member, new_name)

            # If successful add some text to embed message
            message.add_field(name="", value=f'"{_member.mention}" was successfully renamed.', inline=True)
            message.set_thumbnail(url=_member.avatar.url)
            return await ctx.followup.send(embed=message, ephemeral=True)
        else:
            # Send failure message
            message.add_field(name="", value=f"Failed to rename {_member.mention}", inline=True)
            return await ctx.followup.send(embed=message, ephemeral=True)

    # @app_commands.command(name="rank", description=f"This is a description")
    # async def _rank(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="reward", description=f"This is a description")
    # async def _reward(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="ribbon", description=f"This is a description")
    # async def _ribbon(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="bar", description=f"This is a description")
    # async def _bar(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="appoint", description=f"This is a description")
    # async def _appoint(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="promote", description=f"This is a description")
    # async def _promote(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="demote", description=f"This is a description")
    # async def _demote(self, ctx: discord.Interaction, member: str):
    #     pass

    # @app_commands.command(name="loa", description=f"This is a description")
    # async def _leave(self, ctx: discord.Interaction, member: str):
    #     pass

    # AUTO COMPLETION --------------------------------------------------------------------------------------------------

    @_screen.autocomplete('platform')
    async def _find_platforms(self, interaction: discord.Interaction, current: str):
        current_platforms = self.client.settings.get_platforms()
        return \
            [
                app_commands.Choice(name=expected_platform, value=str(platform_id))
                for expected_platform, platform_id in current_platforms.platform.items()
                if current.lower() in expected_platform.lower()
            ][:25]

    @_screen.autocomplete('member')
    async def _find_none_members(self, interaction: discord.Interaction, current: str):
        guild = interaction.guild
        user_id = interaction.user.id

        # Users already in the database
        try:
            rows = await asyncio.to_thread(self._member_access.get_members)
        except Exception as err:
            print(f"DB error in autocomplete: {err}")
            return []
        db_members = {int(row[0]) for row in rows}

        def is_valid(member: discord.Member) -> bool:
            if member.bot or member.id == user_id:
                return False
            if member.id in db_members:
                return False
            return True

        results = []

        if current:
            current_lower = current.lower()

            queried = await guild.query_members(
                query=current,
                limit=100,
                cache=True
            )

            exact, starts, contains = [], [], []

            for m in queried:
                if not is_valid(m):
                    continue

                name = m.display_name.lower()

                if name == current_lower:
                    exact.append(m)
                elif name.startswith(current_lower):
                    starts.append(m)
                elif current_lower in name:
                    contains.append(m)

                if len(exact) + len(starts) + len(contains) >= 25:
                    break

            results = exact + starts + contains

        else:
            # No input: return up to 25 users who are NOT in the database
            for m in guild.members:
                if is_valid(m):
                    results.append(m)

                if len(results) >= 25:
                    break

            results.sort(key=lambda m: m.display_name.lower())

        return [
            app_commands.Choice(
                name=m.display_name,
                value=str(m.id)
            )
            for m in results[:25]
        ]

    @_enlist.autocomplete("member")
    @_rename.autocomplete("member")
    async def _find_members(self, interaction: discord.Interaction, current: str):
        guild = interaction.guild
        user_id = interaction.user.id

        # Users already in the database
        try:
            rows = await asyncio.to_thread(self._member_access.get_members)
        except Exception as err:
            print(f"DB error in autocomplete: {err}")
            return []
        db_members = {int(row[0]) for row in rows}

        def is_valid(member: discord.Member) -> bool:
            if member.bot:
                return False

            if member.id == user_id:
                return False

            # ONLY members that are in the database
            if member.id not in db_members:
                return False

            return True

        results = []

        if current:
            current_lower = current.lower()

            queried = await guild.query_members(
                query=current,
                limit=100,
                cache=True
            )

            exact, starts, contains = [], [], []

            for member in queried:
                if not is_valid(member):
                    continue

                name = member.display_name.lower()

                if name == current_lower:
                    exact.append(member)
                elif name.startswith(current_lower):
                    starts.append(member)
                elif current_lower in name:
                    contains.append(member)

            results = exact + starts + contains

        else:
            # No input: show database members
            for member in guild.members:
                if is_valid(member):
                    results.append(member)

                if len(results) >= 25:
                    break

            results.sort(key=lambda m: m.display_name.lower())

        return [
            app_commands.Choice(
                name=member.display_name[:100],
                value=str(member.id)
            )
            for member in results[:25]
        ]

    # ERROR CHECKING ---------------------------------------------------------------------------------------------------

    @_screen.error
    @_enlist.error
    @_rename.error
    async def _error(self, ctx, error):
        file = None
        warning = None
        support = self.client.settings.get_developer()

        embed = discord.Embed(
            title="ERROR",
            color=discord.Color.darker_grey()
        )

        # Check for errors
        if isinstance(error, discord.app_commands.CommandInvokeError):
            error = error.original
        if isinstance(error, MemberExists):
            warning = "warning"
            embed.title = f"Member Error"
            embed.add_field(name="Message", value=str(error), inline=False)
            embed.color = discord.Color.yellow()
        elif isinstance(error, AuthorizationError):
            warning = "warning"
            required_roles = ("\n".join(
                f"{i}. <@&{role_id}>" for i, role_id in enumerate(error.roles, start=1)
            ))
            embed.title = "Authorisation Error"
            embed.add_field(name="Issues", value=str(error), inline=False)
            embed.add_field(name="Required Roles", value=required_roles, inline=False)
            embed.color = discord.Color.yellow()
        elif isinstance(error, Exception):
            warning = "critical"
            embed.title = "Unexpected Error"
            embed.add_field(name="Message", value=str(error), inline=False)
            embed.add_field(name="Contact", value=f'Please contact: <@{support}>', inline=False)
            embed.color = discord.Color.red()

        embed.set_footer(text="By Order of LATIMER")

        # Set the thumbnail if any
        if warning is not None:
            path = os.path.join(ASSET_ROOT, "warnings", f"{warning}.png")
            if os.path.exists(path):
                file = discord.File(path, filename=f"{warning}.png")
                embed.set_thumbnail(url=f"attachment://{warning}.png")
        else:
            file = None

        # Send message based on response type
        if not ctx.response.is_done():
            await ctx.response.send_message(embed=embed, file=file, ephemeral=True)
        else:
            await ctx.followup.send(embed=embed, file=file, ephemeral=True)

    async def has_authorisation(self, ctx: discord.Interaction) -> bool:
        user = ctx.user
        command = ctx.command.name
        auth_roles = self.client.settings.get_authorized_roles(command)

        user_roles = \
            (
                [role.id for role in user.roles]
                if isinstance(user, discord.Member)
                else []
            )

        if not any(role in auth_roles for role in user_roles):
            raise AuthorizationError("You are not authorized to use this command.", auth_roles)
        return True

async def setup(client: commands.Bot):
    await client.add_cog(Ranker(client))
