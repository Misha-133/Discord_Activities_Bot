import discord_slash
from discord.ext import commands
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_button, create_actionrow
from discordTogether import DiscordTogether
from discord_slash import SlashCommand
import discord
import json


config = {}
messages = {}


cli = commands.Bot(command_prefix="//")
slash = SlashCommand(client=cli, sync_commands=True)
togetherControl = DiscordTogether(cli)

print('Loading configs...')

def loadConfigs():
    global messages
    global config

    try:
        with open("config.json", mode="r", encoding="utf8") as file:
            config = json.load(file)
    except FileNotFoundError:
        print("Config file not found.")
        exit("Critical error")

    try:
        with open(config['messages_file'], mode="r", encoding="utf8") as file:
            messages = json.load(file)
    except FileNotFoundError:
        print("Messages file not found.")
        exit("Critical error")


loadConfigs()


async def updatePresence():
    await cli.change_presence(activity=discord.Game("Working on " + str(len(cli.guilds)) + "servers"))


@cli.event
async def on_ready():
    print(f"Logged into {cli.user}")
    await updatePresence()


@slash.slash(name="reload-config", description="Reload bot config. Some changes will be applied only after restart")
async def reload(ctx: discord_slash.SlashContext):
    loadConfigs()
    await ctx.send(embed=discord.Embed(title=messages['config_reload'], color=int(config['embed_color'], 16)))


@slash.subcommand(base="activity", name="youtube", description=messages['yt_desc'])
async def youtube(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice.channel  is None:
        await ctx.send(embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "youtube", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
    except:
        await ctx.send(
            embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        return


@slash.subcommand(base="activity", name="chess", description=messages["chess_desc"])
async def youtube(ctx: discord_slash.SlashContext):
    await ctx.defer()
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send(embed=discord.Embed(title=messages['error_dm'], color=int(config['error_embed_color'], 16)))
        return
    elif ctx.author.voice.channel is None:
        await ctx.send(
            embed=discord.Embed(title=messages['error_not_in_vc'], color=int(config['error_embed_color'], 16)))
        return
    try:
        link = await togetherControl.create_link(ctx.author.voice.channel.id, "chess", max_age=int(config['link_duration']))
        await ctx.send(embed=discord.Embed(title=messages['your_link'], color=int(config['embed_color'], 16)),
                       components=[create_actionrow(create_button(ButtonStyle.URL, messages['join_activity'], url=str(link)))])
    except:
        await ctx.send(
            embed=discord.Embed(title=messages['int_error'], color=int(config['error_embed_color'], 16)))
        return


if __name__ == '__main__':
    print('Loaded configs, starting bot...')

    cli.run(config['bot_token'])