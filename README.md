# Discord_Activities_Bot
Simple discord activities bot. Allows to start activities in your VCs

This bot adds slash commands on your server which allows you to use DiscordTogether Activities

You can use bot I host - https://misha133.ru/activities_bot/

# Requirements 
Python 3.8+

discord.py 1.7.3

discord-py-slash-command

discord-together

# Installation
Install all needed libs => pip install -r requirements.txt

Create a new application on Discord Developer Portal

Create bot

Copy its token and put it into config.json => "bot_token": "TOKEN_HERE"

Create oauth link with scopes "bot" and "applications.commands" and "Create instant invite" permission

Invite bot to your server and paste link in messages_**.json => "invite_url": "LINK_HERE"

Run main.py


# Possible Problems and Solutions
- "Bot works everywhere except one channel"
Bot need to see VC to create link, so probably it can't see that channel

- "I've just created my own bot - but there's no commands."
Bot uses global slash commands and they take up to 1 hour to register (this is Discord's limitation)
