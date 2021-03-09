import datetime
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import guild_only, has_permissions
import time
import sqlite3
import re


class WelcomeCog(commands.Cog, name='Welcome'):

    def __init__(self, client):

        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        main = sqlite3.connect('main.sqlite')
        cursor = main.cursor()
        embed = discord.Embed(color=0x95efcc, description=f"Welcome to my discord server! You are now #{len(list(member.guild.members))} on our member list!", )
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        channel = client.get_channel(id=815697254479560705)

        await channel.send(embed=embed)


def setup(client):
    client.add_cog(WelcomeCog(client))
    print("Welcome is loaded.")