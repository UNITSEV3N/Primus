
import discord
import unicodedata

async def set_nickname(member: discord.Member, name: str, code: str = "N/A", abbr: str = "N/A"):
    name_length = 19

    if len(name) > name_length:
        raise ValueError(f"Nickname: '{name}' exceeds the {name_length} character limit.")
    try:
        name = unicodedata.normalize("NFC", name)
        structured_name = f"│{code}║{abbr}.│{name}"
        await member.edit(nick=structured_name)
    except discord.Forbidden as err:
        print(f"Missing permissions to change nickname for {member.display_name}: {err}")
        raise
    except discord.HTTPException as err:
        print(f"Discord API error when setting nickname: {err.status} - {err.text}")
        raise
