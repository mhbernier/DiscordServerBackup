
import json
import lzma
import base64
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
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_footer(text="⛔ You are not authorized to use this bot")
        await ctx.send(embed=embed, delete_after=6.0)
        await ctx.message.delete()
        raise commands.CommandError


# TODO Add more fields
@bot.command()
async def server_stats(ctx: commands.Context):

    server = ctx.guild

    embed = discord.Embed(title=f"{server.name} Stats", color=discord.Colour.blue())
    embed.add_field(name="Creation date", value=str(server.created_at), inline=False)

    await ctx.send(embed=embed, delete_after=12.0)


@bot.command()
async def backup_users(ctx: commands.Context):

    member: discord.Member
    server: discord.Guild = ctx.guild
    users_list = list()
    banned_members = await server.bans()
    server_members_count = len(server.members)
    banned_members_count = len(banned_members)
    ts = datetime.datetime.now().timestamp()

    with open(f'users - {ts}.json', 'w', encoding='utf-8') as users_json:

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

    embed = discord.Embed(title=f"{server.name} Members", color=discord.Colour.blue())
    embed.add_field(name="Members", value=str(server_members_count), inline=False)
    embed.add_field(name="Banned members", value=str(banned_members_count), inline=False)
    embed.set_footer(text="✅ Guild users backed up")

    await ctx.send(embed=embed, delete_after=12.0)


@bot.command()
async def backup_category(ctx: commands.Context, category_name: str):

    message: discord.Message
    channel: discord.TextChannel
    attachment: discord.Attachment
    category: discord.CategoryChannel

    server: discord.Guild = ctx.guild
    messages_count = 0
    channels_count = 0
    counter = 1

    for category in server.categories:
        if category.name.lower() == category_name.lower():

            channels_count = len(category.text_channels)

            for channel in category.text_channels:

                channel_messages = await channel.history(limit=None).flatten()
                messages_count += len(channel_messages)
                ts = datetime.datetime.now().timestamp()

                with open(f'{channel.name} - {ts}.json', 'w+', encoding='utf-8') as messages_json:

                    attachments = list()

                    for message in channel_messages:

                        for attachment in message.attachments:
                            data = base64.b64encode(await attachment.read()).decode('ascii')
                            attachments.append({
                                "id": attachment.id,
                                "size": attachment.size,
                                "filename": attachment.filename,
                                "content": data
                            })

                        message_json = {
                            "id": message.id,
                            "author": message.author.id,
                            "content": message.clean_content,
                            "attachments": attachments
                        }

                        messages_json.write(json.dumps(message_json, sort_keys=True, indent=4))

                    embed = discord.Embed(color=discord.Colour.green())
                    embed.set_footer(text=f"✅ [{counter}/{channels_count}] {channel.name}")
                    await ctx.send(embed=embed, delete_after=12.0)

                    counter += 1

            embed = discord.Embed(title=f"{server.name} - {category_name}", color=discord.Colour.blue())
            embed.add_field(name="Messages", value=str(messages_count), inline=False)
            embed.add_field(name="Channels", value=str(channels_count), inline=False)
            embed.set_footer(text=f"✅ Category backed up")

            await ctx.send(embed=embed, delete_after=12.0)

            return

    embed = discord.Embed(color=discord.Colour.red())
    embed.set_footer(text=f"The category {category_name} doesn't exist")
    await ctx.send(embed=embed, delete_after=6.0)


if __name__ == '__main__':
    with open('token.txt', 'r') as token_file:
        bot.run(token_file.read())
