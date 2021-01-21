
import json
import datetime

import discord
from discord.ext import commands

description = "A Discord bot to backup the content of your server."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='>> ', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")


@bot.event
async def on_command_completion(ctx: commands.Context):
    await ctx.message.delete()


@bot.before_invoke
async def before_command(ctx):
    if not await bot.is_owner(ctx.message.author):
        raise commands.CommandError


@bot.command()
async def backup_users(ctx: commands.Context):

    member: discord.Member
    server: discord.Guild = ctx.message.guild
    users_list = list()
    banned_members = await server.bans()
    server_members_count = len(server.members)
    banned_members_count = len(banned_members)
    ts = datetime.datetime.now().timestamp()

    with open(f'{server.name} Users - {ts}.json', 'w', encoding='utf-8') as users_json:

        for member in server.members:
            if not member.bot:
                users_list.append({
                    "id": member.id,
                    "name": member.name,
                    "discriminator": member.discriminator,
                    "banned": False
                })

        for ban_entry in banned_members:
            users_list.append({
                "id": ban_entry.user.id,
                "name": ban_entry.user.name,
                "discriminator": ban_entry.user.discriminator,
                "banned": True
            })

        users_json.write(json.dumps(users_list, sort_keys=True, indent=4))

    embed = discord.Embed(title=f"{server.name} Members", color=0x207dff)
    embed.add_field(name="Members", value=str(server_members_count), inline=False)
    embed.add_field(name="Banned members", value=str(banned_members_count), inline=False)

    await ctx.send("Guild users backed up :white_check_mark:", embed=embed, delete_after=15.0)


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
