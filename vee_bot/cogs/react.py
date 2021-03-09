
import discord
from discord.ext import commands
import asyncio
import datetime
import re
import sqlite3


class ReactCog(commands.Cog, name='Reactions'):

    def __init__(self, client):

        self.client = client
        

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id and emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)
            if result is None:
                return
            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)               
                await user.add_role(on)
            else:
                return                
        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id and emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)
            if result is None:
                return
            elif result is not None:
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)               
                await user.add_role(on)
            else:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        if '<:' in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id and emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)
            if result is None:
                return
            elif str(reaction.emoji.id) in str(result[0]):
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)               
                await user.remove_roles(on)
            else:
                return                
        elif '<:' not in str(reaction.emoji):
            cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id and emoji = '{reaction.emoji.id}'")
            result = cursor.fetchone()
            guild = self.client.get_guild(reaction.guild_id)
            if result is None:
                return
            elif result is not None:
                on = discord.utils.get(guild.roles, id=int(result[1]))
                user = guild.get_member(reaction.user_id)               
                await user.remove_roles(on)
            else:
                return

    @commands.command()
    async def roleadd(self, ctx, channel:discord.TextChannel, messageid, emoji, role:discord.Role):
        main = sqlite3.connect('main.db')
        cursor = main.cursor()
        cursor.execute(f"SELECT emoji, role, message_id, channel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id and emoji = '{reaction.emoji.id}'")
        result = cursor.fetchone()
        if '<:' in emoji:
            emm = re.sub(':.*?:', '', emoji).strip('<>')
            if result is None:
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guil_id) VALUES(?,?,?,?,?)')
                VAL = (emm, role.id, message.id, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                em = self.client.get_emoji(int(emm))
                await msg.add_reactions(em)
            elif str(messageid) not in str(result[3]):
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guil_id) VALUES(?,?,?,?,?)')
                VAL = (emm, role.id, message.id, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                em = self.client.get_emoji(int(emm))
                await msg.add_reactions(em)

        elif '<:' not in emoji:
            if result is None:
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guil_id) VALUES(?,?,?,?,?)')
                VAL = (emoji, role.id, message.id, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reactions(emoji)
            elif str(messageid) not in str(result[3]):
                sql = ('INSERT INTO reaction(emoji, role, message_id, channel_id, guil_id) VALUES(?,?,?,?,?)')
                VAL = (emoji, role.id, message.id, channel.id, ctx.guild.id)
                msg = await channel.fetch_message(messageid)
                await msg.add_reactions(emoji)
        cursor.execute(sql, val)
        main.commit()
        cursor.close()
        main.close()

def setup(client):
    client.add_cog(ReactCog(client))
    print("React is loaded.")
