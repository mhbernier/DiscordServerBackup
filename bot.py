# This example requires the 'members' privileged intents

import discord
from discord.ext import commands

description = "A Discord bot to backup the content of your server."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


@bot.command()
async def backup_users(ctx: commands.Context):
    await ctx.send("Command is not implemented yet.")


@bot.command()
async def backup_channel(ctx: commands.Context):
    await ctx.send("Command is not implemented yet.")


@bot.command()
async def backup_channels(ctx: commands.Context):
    await ctx.send("Command is not implemented yet.")


@bot.command()
async def backup_structure(ctx: commands.Context):
    await ctx.send("Command is not implemented yet.")


if __name__ == '__main__':
    with open('token.txt', 'r') as token_file:
        bot.run(token_file.read())
