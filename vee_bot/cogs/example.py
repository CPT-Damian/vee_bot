import datetime
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import guild_only, has_permissions
import time
import sqlite3
import re
from discord.ext.commands.cooldowns import BucketType

client = commands.Bot(command_prefix='v!', help_command=None)

global spam
spam = False
x = False
rate = 1
per = 60
t = BucketType.default


class Example(commands.Cog):

    def __init__(self, client):

        self.message = None
        self.client = client
        self.states = {}
        self.whitelist = [628732881707073547, 639568185099681802, 710672487414890627]


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.idle, activity=discord.Game('v!'))
        print('Logged in as {} - {}'.format(self.client.user.name, self.client.user.id))
        


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))

    @commands.Cog.listener()
    async def on_member_remove(self, member, ctx):
        ctx.send(f'{member} has left the server')

    
    @commands.Cog.listener()
    async def on_message(self, message: str):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        with open("/home/hellhound/PycharmProjects/pythonProject/vee_bot/logs/chatlogs.txt", "a") as text_file:
            print(f"{message.channel} <{st}> {message.author} {message.content} {message.attachments}", file=text_file)

    @commands.command(
        name="ping",
        description="Shows my ping.",
        usage=""
    )
    async def ping(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(title=None, description='My ping is: {}ms'.format(round((t2 - t1) * 1000)), color=0x2874A6)
        await channel.send(embed=embed)

    @commands.command(
        name="info",
        description="Shows info on a member",
        usage="<user>"
    )
    async def info(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    # This kicks whoever you tag. Also let's you add a reason Eg: ~kick Jones#9000 Breaking Discord TOS
    @commands.command(
        name="kick",
        description="Kicks member from server",
        usage="<user>"
    )
    async def kick(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        channel = ctx.message.channel
        if author.guild_permissions.kick_members:
            if member is None:
                await channel.send('Please input a user.')
            else:
                await channel.send("**{}** has been kicked.".format(member.name))
                await member.kick()
        else:
            await channel.send('You lack permission to perform this action')

    # Clears chat with given value
    @commands.command(
        name="clear",
        description="Specify amount of logs to clear. Clears 10 if not specified.",
        usage="<amount>"
    )
    async def clear(self, ctx, amount=10):
        user = ctx.message.author
        channel = ctx.message.channel
        messages = []
        async for message in channel.history(limit=int(amount)):
            messages.append(message)
        await channel.delete_messages(messages)
        await channel.send(f'{user.mention} Messages deleted')


    @commands.command(
        name="mute",
        description="Mutes member in server",
        usage="<user>"
    )
    @has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = "No reason provided"
        if member == None or member == ctx.message.author:
            await ctx.channel.send("**You cannot mute yourself.**")
            return
        if member.guild_permissions.manage_messages == True:
            await ctx.send("**This user is a mod.**")
            return
        else:
            guild = ctx.guild
            mutedRole = discord.utils.get(guild.roles, name="Muted")

            if not mutedRole:
                mutedRole = await guild.create_role(name="Muted")

                for channel in guild.channels:
                    await channel.set_permissions(mutedRole, speak=False, send_messages=False,
                                                  read_message_history=True, read_messages=False)
            await ctx.channel.send(f"***{member} has been muted. Reason: " + reason + "***")
            await member.add_roles(mutedRole, reason=reason)
            server = ctx.message.guild.name
            await member.send("You were muted from " + server + ". Reason: " + reason)

    @commands.command(
        name="ban",
        description="Bans member from server.",
        usage="<user>"
    )

    async def ban(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        channel = ctx.message.channel
        if author.guild_permissions.kick_members:
            if member is None:
                await channel.send('Please input a user.')
            else:
                await channel.send("Get banned **{}**, Damn kid".format(member.name))
                await member.ban()
        else:
            await channel.send('You lack permission to perform this action')

    # This Unbans a member
    @commands.command(
        name="unban",
        description="Unbans member from server.",
        usage="<user>"
    )
    @guild_only()
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(f'{user.mention} welcome back! PLease make sure to read the #rules to avoid being banned.')

    @commands.command()
    async def addcha(self, ctx, channel_name):
        await ctx.guild.create_text_channel(channel_name)
        embed = discord.Embed(color=0x95efcc, description=f"```Channel, **{channel_name}** was created!```")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Example(client))
    print("Moderation is loaded.")


