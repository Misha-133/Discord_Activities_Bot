import datetime
import discord_slash
from discord.ext import commands
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discordTogether import DiscordTogether
from discord_slash import SlashCommand
import discord
import json
import os


config = {}
messages = {}


cli = commands.Bot(command_prefix="/")
slash = SlashCommand(client=cli, sync_commands=False)
togetherControl = DiscordTogether(cli)

print('Loading configs...')
started = datetime.datetime.now()


def loadConfigs():
    global messages
    global config

    try:
        with open("config.json", mode="r", encoding="utf8") as file:
            config = json.load(file)
    except FileNotFoundError:
        log("Config file not found.")
        exit("Critical error")

    try:
        with open(config['messages_file'], mode="r", encoding="utf8") as file:
            messages = json.load(file)
    except FileNotFoundError:
        log("Messages file not found.")
        exit("Critical error")


loadConfigs()


def log(*args):
    print(f"[{datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S')}]", *args)
    with open(f"logs/log_{started.strftime('%m-%d-%Y;%H-%M')}.txt", mode="a", encoding="utf8") as file:
        print(f"[{datetime.datetime.now().strftime('%m.%d.%Y %H:%M:%S')}]", *args, file=file)


async def updatePresence():
    await cli.change_presence(activity=discord.Game("Working on " + str(len(cli.guilds)) + " servers"))


@cli.event
async def on_ready():
    log(f"Logged into {cli.user}")
    await updatePresence()


@slash.slash(name="reload-config", description=messages['reload_desc'])
async def reload(ctx: discord_slash.SlashContext):
    loadConfigs()
    await ctx.send(embed=discord.Embed(title=messages['config_reload'], color=int(config['embed_color'], 16)))


@slash.slash(name="invite-link", description=messages['invite_desc'])
async def reload(ctx: discord_slash.SlashContext):
    await ctx.send(embed=discord.Embed(title=messages['invite_emb'], color=int(config['embed_color'], 16)),
                   hidden=True, components=[create_actionrow(create_button(ButtonStyle.URL, messages['invite_btn'],
                                                                           url=messages['invite_url']))])


@slash.subcommand(base="activity", name="youtube", description=messages['yt_desc'])
async def youtube(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "youtube", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(
            embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="chess", description=messages["chess_desc"])
async def chess(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "chess", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="poker", description=messages["poker_desc"])
async def poker(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "poker", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="betrayal", description=messages["betrayal_desc"])
async def betrayal(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "betrayal", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="fishing", description=messages["fishing_desc"])
async def fishing(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "fishing",
                                                 max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="letter-tile", description=messages["letter-tile_desc"])
async def letterTile(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "letter-tile",
                                                 max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="word-snack", description=messages["word-snack_desc"])
async def wordSnack(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "word-snack",
                                                 max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[
                           create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@slash.subcommand(base="activity", name="doodle-crew", description=messages["doodle-crew_desc"])
async def doodleCrew(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "doodle-crew",
                                                 max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[
                           create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
        log(f"{ctx.author} created link {str(link)} on guild {ctx.guild.name}")
    except Exception as ex:
        await ctx.send(embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        log(ex)
        return


@cli.event
async def on_guild_join(guild: discord.Guild):
    log(f'Joined {guild.name}')
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
