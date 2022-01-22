import datetime
import discord_slash
import discord_together.errors
from discord.ext import commands
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.utils.manage_commands import create_permission, add_slash_command, create_choice, create_option, get_all_commands, remove_all_commands_in
from discord_together import DiscordTogether
from discord_slash import SlashCommand
import discord
import json
import os
from discord_slash.model import SlashCommandPermissionType, SlashCommandOptionType


config = {}
messages = {}
guild_ids = []
activities = {}


cli = commands.Bot(command_prefix="//")
slash = SlashCommand(client=cli, sync_commands=False)


print('Loading configs...')
started = datetime.datetime.now()


def loadConfigs():
    global messages
    global config
    global activities

    try:
        with open("config.json", mode="r", encoding="utf8") as file:
            config = json.load(file)
        with open("activities.json", mode="r", encoding="utf8") as file:
            activities = json.load(file)
        with open(config['messages_file'], mode="r", encoding="utf8") as file:
            messages = json.load(file)
    except FileNotFoundError:
        log("Config file not found.")
        exit("Critical error")


loadConfigs()


async def createActivityLink(ctx: discord_slash.SlashContext, activity: str):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await disTogether.create_link(ctx.author.voice.channel.id, activity,
                                                 max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_activity'],
                                           description='`' + activities[activity] + '`',
                                           color=int(config['embed_color'], 16)),
                       components=[
                           create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name} - {activities[activity]}")
    except discord_together.errors.BotMissingPerms:
        await ctx.send(embed=discord.Embed(title=messages['missing_perms'], color=int(config['error_embed_color'], 16)))
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


def log(*args):
    print(f"[{datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S')}]", *args)
    with open(f"logs/log_{started.strftime('%m-%d-%Y;%H-%M')}.txt", mode="a", encoding="utf8") as file:
        print(f"[{datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S')}]", *args, file=file)


async def updatePresence():
    await cli.change_presence(activity=discord.Game("Working on " + str(len(cli.guilds)) + " servers"))


@cli.event
async def on_connect():
    global guild_ids
    guild_ids = [g.id for g in cli.guilds]


@cli.event
async def on_ready():
    global disTogether

    log(f"Logged into {cli.user}")
    await updatePresence()

    disTogether = await DiscordTogether(config['bot_token'])
    for g in cli.guilds:
        g: discord.Guild

        await addCommands(g)

    log(f"Initialised on {len(cli.guilds)} guilds")


@slash.slash(name='activity', description=messages['activity_desc'], guild_ids=guild_ids,
             options=[create_option(name="activity", description="Choose activity", option_type=SlashCommandOptionType.STRING, required=True,
                                    choices=[create_choice(act, activities[act]) for act in activities.keys()])])
async def aboba(ctx: discord_slash.SlashContext, activity: str):
    await createActivityLink(ctx, activity)


@slash.slash(name="reload-config", description=messages['reload_desc'],
             permissions={config['admin_guild_id']: [create_permission(config['admin_id'], SlashCommandPermissionType.USER, True)]},
             guild_ids=[int(config['admin_guild_id'])])
async def reload(ctx: discord_slash.SlashContext):
    loadConfigs()
    await ctx.send(embed=discord.Embed(title=messages['config_reload'], color=int(config['embed_color'], 16)))


@slash.slash(name="invite-link", description=messages['invite_desc'], guild_ids=guild_ids)
async def invite(ctx: discord_slash.SlashContext):
    await ctx.send(embed=discord.Embed(title=messages['invite_emb'], color=int(config['embed_color'], 16)),
                   hidden=True, components=[create_actionrow(create_button(ButtonStyle.URL, messages['invite_btn'],
                                                                           url=messages['invite_url']))])


@slash.slash(name="help", description=messages['help-com-desc'], guild_ids=guild_ids)
async def help(ctx: discord_slash.SlashContext):
    await ctx.send(embed=discord.Embed(title=messages['help-title'], color=int(messages['help-color'], 16), description=messages['help-desc']))


async def addCommands(guild: discord.Guild):
    commands = [com['name'] for com in await get_all_commands(cli.user.id, config['bot_token'], guild.id)]

    if [True for com in commands if com not in config['command_names']]:
        await remove_all_commands_in(cli.user.id, config['bot_token'], guild.id)

        await add_slash_command(cli.user.id, config['bot_token'], guild.id, "activity", messages['activity_desc'],
                                [create_option(name="activity", description="Choose activity", option_type=SlashCommandOptionType.STRING, required=True,
                                        choices=[create_choice(act, activities[act]) for act in activities.keys()])])

        await add_slash_command(cli.user.id, config['bot_token'], guild.id, "help", messages['help-com-desc'])

        await add_slash_command(cli.user.id, config['bot_token'], guild.id, "invite", messages["invite_desc"])

        log(f"Synced commands on {guild.name}")


@cli.event
async def on_guild_join(guild: discord.Guild):
    log(f'Joined {guild.name}')
    await addCommands(guild)
    await updatePresence()


@cli.event
async def on_guild_remove(guild: discord.Guild):
    log(f'Removed from {guild.name}')
    await updatePresence()


if __name__ == '__main__':
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log('Loaded configs, starting bot...')
    try:
        cli.run(config['bot_token'])
    except discord.LoginFailure:
        log("Invalid Token")
