## Disclaimer
This repository is just my study experience.

I'm trying to show my skill in Python here after years of self-education.

Thanks 💜💙

# Discord bot sample on discord.py
This is a simple bot for your discord servers managed by cogs (modules).

A preinstalled Filter module allows you to manage messages filter for specific servers.
Every server (guild) has its own messages filter and will delete the forbidden words if the author doesn't have the `Manage Messages` permission for this server.
Only members with `Manage Messages` permission can edit the filter.

You can add your modules if you want.
On how to use and build cogs you can find in the [docs for discord.py](https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html#quick-example).

### Commands
| Command        | Arguments           | Description                                                                                                                     |
|:---------------|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------|
| help           |                     | Shows the help message.                                                                                                         |
| log            |                     | Returns the client log for the current session.                                                                                 |
|                |                     |                                                                                                                                 |
| modules        | None or subcommands | If no arguments are provided, invokes `modules list`.                                                                           |
| modules list   |                     | Returns available modules and defines Loaded and Not Loaded modules.                                                            |
| modules load   | Module name         | Loads the module with the following name.                                                                                       |
| modules unload | Module name         | Unloads the module with the following name.                                                                                     |
| modules reload | Module name         | Reloads the module with the following name. Applies all changes in the file. If the module is not loaded invokes `module load`. |
|                |                     |                                                                                                                                 |
| filter         | Subcommands         | Does nothing without subcommands.                                                                                               |
| filter list    |                     | Returns the list of banned words for the current server in DMs.                                                                 |
| filter add     | \*Words             | Adds words to the filter for the current server — separate words with spaces.                                                   |
| filter remove  | \*Words             | Removes words from the filter for the current server.                                                                           |
| filter check   | Text or Message ID  | Checks the provided text (or the message) for the banned words and returns all the triggered words.                             |

## Tech
### Versions
| Library    | Version                                                       |
|:-----------|:-------------------------------------------------------------:|
| Python     | [3.9.9](https://www.python.org/downloads/release/python-399/) |
| discord.py | [1.7.3](https://pypi.org/project/discord.py/1.7.3/)           |

### Missing files
You might have a missing file in this repo - `Bot/config/secret.py`

This file stores the secret token of your bot and looks like this:
```py
token = "YOUR TOKEN HERE"
```

### Instalation and usage
1. Install [the following libraries](#versions)
2. Clone or save this repository anywhere you would like to have it.
3. Add [the missing file with your secret token](#missing-files)
4. Open your terminal (CMD or PowerShell).
5. Go to the repository you have cloned.
6. When you are in `discord-py-Bot-Sample` - Run `Bot/main.py`.
7. Invite the bot to your server.

Members can manage modules with the `Administrator` permission.

Members can use filter module commands with the `Manage Messages` permission.

## P.S.
You can do whatever you want with this repo.

But if it's not hard for you, follow me on [Twitter](https://twitter.com/AnriaruDoragon) ([Work Acc](https://twitter.com/AnriaruDoragon_))

Good luck!
