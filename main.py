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


@cli.event
async def on_ready():
    print(f"Logged into {cli.user}")


@slash.slash(name="activity", description="Start Discord Together activity")
async def activ(ctx: discord_slash.SlashContext):
    pass

@slash.subcommand(base="activity", name="youtube", description="Start Youtube Together activity")
async def youtube(ctx: discord_slash.SlashContext):
    link = await togetherControl.create_link(ctx.author.voice.channel.id, "youtube")
    await ctx.send(embed=discord.Embed(title="Your activity"),
                   components=[create_actionrow(create_button(ButtonStyle.URL, "Join Activity", url=str(link)))])


if __name__ == '__main__':
    print('Loading configs...')

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

    print('Loaded configs, starting bot...')

    cli.run(config['bot_token'])