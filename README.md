<div align="center">

# LATIMER

<table>
  <tr>
    <td width="250" align="center" valign="middle">
      <img src="res/assets/bot/LATIMER_4_1.png" alt="Latimer" width="230">
    </td>
    <td valign="middle">
      Richard J. Latimer (Character Name) was a Lieutenant Colonel in the Enclave Expeditionary Forces, a Fallout 76 Roleplay community. In late 2023, he passed away in real life, and to honor him, his friends have dedicated this bot in his name.
    </td>
  </tr>
</table>

### *Project Primus - A rewrite*

![Discord Bot](https://img.shields.io/badge/Discord-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-library-3776AB?style=for-the-badge&logo=discord&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.14.8-3776AB?style=for-the-badge&logo=python&logoColor=white)
![WSL Debian](https://img.shields.io/badge/WSL-Debian-A81D33?style=for-the-badge&logo=debian&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen?style=for-the-badge)

Latimer is a Discord bot build under the Project Primius. This repository contains the Rewrite, a complete rebuild of legacy systems.

`An attempt to create a modular Discord bot for a Fallout 76 RP server.`

### FEATURES

| | Feature | Description |
|---|---|---|
| 🎛️ | **Slash Commands** | Fully built on Discord's application command system |
| ⚙️ | **Server Config** | Configurations for Primary RP server|
| 🔌 | **Hot-Reloadable Modules** | Load, unload, and reload cogs without restarting |

</div>

## Commands

<div align="center">

**Legend:** ✅ Live · 🚧 In progress · 📝 Planned

</div>

### Personnel
- ✅ **`/screen`** – Screen a new recruit: register them with a character name and platform, set their nickname, and assign the Recruit role.
- ✅ **`/rename`** – Change a member's character name and sync their Discord nickname.
- 🚧 **`/enlist`** – Enlist a screened recruit into the ranks.
- 📝 **`/rank`** – View a member's current rank and service record.
- 📝 **`/promote`** – Promote a member to the next rank.
- 📝 **`/demote`** – Demote a member to a lower rank.
- 📝 **`/appoint`** – Assign a member a specific rank, bypassing promotion restrictions.
- 📝 **`/loa`** – File or manage a leave of absence.

### Awards & Training
- 📝 **`/reward`** – Grant a medal or commendation to a member.
- 📝 **`/ribbon`** – Award a member a training certificate.

### Restrictions
- 📝 **`/bar`** – Bar a member from receiving rewards and promotions.

### Developer *(Owner only)*
- ✅ **`/ping`** – Show the bot's latency.
- ✅ **`/reload`** – Reload all cogs, with an option to re-sync slash commands.
- ✅ **`/nuke_channel`** – Purge all messages in the current channel.
- ✅ **`/shutdown`** – Shut the bot down.

## Installation

1. **Clone the repo**
   ```bash
   git clone -b dev https://github.com/UNITSEV3N/Primus.git
   cd Primus
   ```

2. **Install dependencies**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure the environment**
   ```bash
   cp .env.example .env
   ```
   Fill in your Discord bot token and MySQL credentials.

4. **Configure the environment**
   ```
   Configure server.json and config.json files
   ```

5. **Run the bot**
   ```bash
   python -m bot
   ```

> **Requires:** Python 3.14.8, a running MySQL server, and a Discord bot token with the **Server Members Intent** enabled.

