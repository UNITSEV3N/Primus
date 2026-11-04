
import discord

async def validate_roles(guild: discord.Guild, role_ids: list[int]):
    roles = []
    for role_id in role_ids:
        role = guild.get_role(role_id)
        if role is not None:
            roles.append(role)
    return roles

async def update_roles(ctx: discord.Interaction, member: discord.Member, add: list[int] | None = None, remove: list[int] | None = None):
    roles = None
    target_roles = None
    method = None
    reason = None
    action = None

    if not add and not remove:
        raise ValueError("Invalid arguments: 'add' or 'remove' is required.")

    if add:
        action = "add"
        roles = await validate_roles(ctx.guild, add)
        method = member.add_roles
        reason = f"Added {len(add)} roles"

    if remove:
        action = "remove"
        roles = await validate_roles(ctx.guild, remove)
        method = member.remove_roles
        reason = f"Removed {len(remove)} roles"

    try:
        max_roles_call = 10
        for chunk in range(0, len(roles), max_roles_call):
            chunk_roles = roles[chunk:chunk + max_roles_call]
            await method(*chunk_roles, reason=reason)

    except discord.Forbidden:
        raise PermissionError(f"Bot lacks permission to {action} one or more roles.")
    except discord.HTTPException as e:
        raise RuntimeError(f"Failed to {action} roles: {e}")