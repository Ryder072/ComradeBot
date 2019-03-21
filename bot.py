import discord
from discord.ext import commands
import os
import asyncio

token = os.environ['token']
client = commands.Bot(command_prefix = '!')
client.remove_command('help')

pasta_perm = True
timeout_member = None
#function activate when started
@client.event
async def on_ready():
    print("Spirit woken")
    await client.change_presence(game=discord.Game(name='Food War'))


#commands for the bot with prefix '!'
#this one echoes everything the user says
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)


#clear messages, 10 by default, 100 at max
@client.command(pass_context=True)
async def sweep(ctx, amount=10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel,limit=int(amount),):
        messages.append(message)
    await client.delete_messages(messages)

#custom help command for the retards
@client.command()
async def help():
    embed = discord.Embed(
        colour = discord.Color.orange()
    )

    embed.set_author(name='Set of commands')
    embed.add_field(name="!sweep [# of messages]", value="Clears a set number of messages(10 by default).", inline=False)
    embed.add_field(name='!kick [Member Name]',value='Kicks the member from server', inline=False)
    embed.add_field(name='!redirect [member1][member2] [channel]', value='Redirects members to the given channel', inline=False)
    embed.add_field(name='!timeout [member]', value='Mutes the member for 5 minutes. Only 1 member can be timed out', inline=False)

    await client.say(embed=embed)



#command activated when a new member joins
@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Comrades')
    await client.add_roles(member, role)
    channel = discord.utils.get(member.server.channels, name='general')
    await client.send_message(channel, "Hello there {}. You have been promoted to Comrade rank!".format(member.name))

#only the members with permission to kick members can successfully call this command
@client.command(pass_context=True)
async def kick(ctx, guilty):
    channel = ctx.message.channel
    perms = ctx.message.author.permissions_in(channel).kick_members
    member = discord.utils.get(ctx.message.server.members, name=guilty)
    if member == None:
        await client.say("Traitor not found")
        return
    elif perms:
        await client.kick(member)
        await client.say("Off to the gulag they go!")
    else:
        await client.say("Back off Comrade! :triumph: You can't kick other members")

#redirect users to a certain channel
@client.command(pass_context=True)
async def redirect(ctx, member1, member2, channel):
    user1 = discord.utils.get(ctx.message.server.members, name=member1)
    user2 = discord.utils.get(ctx.message.server.members, name=member2)
    chan = discord.utils.get(ctx.message.server.channels, name=channel)

    if user1 and user2:
        if chan:
            await client.send_message(chan, "{},{} continue conversation in this channel.".format(user1.mention,user2.mention))
        else:
            await client.say("Wrong channel")
    else:
        await client.say("Comrades not found")


#any messages by the user are deleted for 5 minutes
@client.command(pass_context=True)
async def timeout(ctx, member):
    channel = ctx.message.channel
    perms = ctx.message.author.permissions_in(channel).administrator
    if not perms:
        await client.say("You can't timeout members")
        return
    memb = discord.utils.get(ctx.message.server.members, name=member)
    global timeout_member
    timeout_member = memb
    await client.say("Comrade {} has been timed out for 5 minutes".format(memb.name))
    await out(memb)

#the function to calculate time elapsed
async def out(member):
    global timeout_member
    amount = 5
    while amount!=0:
        await asyncio.sleep(60)
        amount-=1
    timeout_member = None





client.run(token)
