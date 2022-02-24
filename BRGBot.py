import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('BRG Bot ({0.user}) is active.'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='BRG'))

@bot.command()
async def ping(ctx):
    embed=discord.Embed(description=f'Pong! My ping is **{round(bot.latency * 1000)}**ms.', color=0xABCDEF)
    await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def embed(ctx, *, message):
    embed=discord.Embed(description=message, color=0xABCDEF)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user : discord.Member, *, reason=None):
    if reason == None:
        embed=discord.Embed(description=f'**{user.mention}** has been *kicked* from the server.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been *kicked* from **BRG Official**.', color=0xABCDEF)
        await ctx.send(embed=embed)
        await user.send(embed=dmEmbed)
    else:
        embed=discord.Embed(description=f'**{user.mention}** has been *kicked* from the server for __{reason}__.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been *kicked* from **BRG Official** for __{reason}__.', color=0xABCDEF)
        await ctx.send(embed=embed)
        await user.send(embed=dmEmbed)
    await user.kick(reason=reason)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    if reason == None:
        embed=discord.Embed(description=f'{member.mention} has been *banned* from the server.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been *banned* from **BRG Official**.', color=0xABCDEF)
        await member.send(embed=dmEmbed)
        await ctx.send(embed=embed)
    else:
        embed=discord.Embed(description=f'{member.mention} has been *banned* from the server for __{reason}__.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been *banned* from **BRG Official** for __{reason}__.', color=0xABCDEF)
        await ctx.send(embed=embed)
        await member.send(embed=dmEmbed)
    await member.ban(reason=reason)

@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    embed=discord.Embed(description=f'**{member}** has been *unbanned* from the server.', color=0xABCDEF)
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, user : discord.Member, *, reason=None):
    if reason == None:
        embed=discord.Embed(description=f'{user.mention} has been *warned*.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been warned on **BRG Official**.', color=0xABCDEF)
        await ctx.send(embed=embed)
        await user.send(embed=dmEmbed)
    else:
        embed=discord.Embed(description=f'{user.mention} has been *warned* for __{reason}__.', color=0xABCDEF)
        dmEmbed=discord.Embed(description=f'You have been warned on **BRG Official** for __{reason}__.', color=0xABCDEF)
        await ctx.send(embed=embed)
        await user.send(embed=dmEmbed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member : discord.Member):
    MutedRole=discord.utils.get(ctx.guild.roles, name='Muted')
    if not MutedRole:
        MutedRole = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(MutedRole, speak=False, send_messages=False, read_message_history=True)
    embed=discord.Embed(description=f'{member.mention} was *muted*.', color=0xABCDEF)
    dmEmbed=discord.Embed(description=f'You were *muted* on **BRG Official**.', color=0xABCDEF)
    await member.add_roles(MutedRole)
    await ctx.send(embed=embed)
    await member.send(embed=dmEmbed)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member : discord.Member):
    MutedRole = discord.utils.get(ctx.guild.roles, name='Muted')
    embed1=discord.Embed(description=f'{member.mention} has been **unmuted** from the server.', color=0xABCDEF)
    embed2=discord.Embed(description=f'You have been **unmuted** from **BRG Official**.', color=0xABCDEF)
    await member.remove_roles(MutedRole)
    await ctx.send(embed=embed1)
    await member.send(embed=embed2)

@bot.command(aliases = ['purge', 'clean'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int = 999999999):
    await ctx.channel.purge(limit = amount + 1)
    await asyncio.sleep(0.2)
    if amount == 999999999:
        embed = discord.Embed(description = f'Cleared {ctx.message.channel.mention}.', color = 0x00FF00)
        await ctx.send(embed=embed, delete_after=5)
    else:
        embed = discord.Embed(description = f'Cleared **{amount}** messages in {ctx.message.channel.mention}.', color = 0x00FF00)
        await ctx.send(embed=embed, delete_after=5)

@bot.command(aliases = ['editnick', 'nick'])
@commands.has_permissions(manage_nicknames=True)
async def changenick(ctx, user : discord.Member, *, nick):
    await user.edit(nick=nick)
    await ctx.send(f"Changed **{user}**'s nickname to **{user.display_name}**!")

@bot.command(aliases = ['editroles', 'roles'])
@commands.has_permissions(manage_roles=True)
async def changeroles(ctx, addorremove, user : discord.Member, role : discord.Role):
    if addorremove == 'add' or addorremove == 'Add':
        await user.add_roles(role)
        await ctx.send(f"Added **{role}** to {user.display_name}'s roles.")
    elif addorremove == 'remove' or addorremove == 'Remove':
        await user.remove_roles(role)
        await ctx.send(f"Removed **{role}** from {user.display_name}'s roles.")
    elif addorremove != 'add' and addorremove != 'remove' and addorremove != 'Add' and addorremove != 'Remove':
        await ctx.send('Please use the command in this form: `*changeroles [add/remove] [user] [role]`.')

@bot.command(aliases=['staffping', 'helpstaff', 'pingstaff', 'adminping', 'adminhelp', 'pingadmin'])
@commands.cooldown(1, 1800, commands.BucketType.user)
async def staffhelp(ctx):
    await ctx.send('Pinging <@&830822953095790602>!')

@bot.command(aliases = ['av', 'pfp', 'profilepicture', 'useravatar'])
async def avatar(ctx, user : discord.Member = None):
    if user == None:
        embed = discord.Embed(color = 0xABCDEF)
        embed.set_author(name=f"{ctx.author}'s avatar")
        embed.set_image(url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(color = 0xABCDEF)
        embed.set_author(name=f"{user.display_name}'s avatar")
        embed.set_image(url=user.avatar_url)
        await ctx.reply(embed=embed)

@bot.command(aliases=['dm'])
@commands.has_any_role(763773648662167642)
async def directmessage(ctx, recipient : discord.Member, *, message):
    if ctx.author.guild.id == recipient.guild.id:
        embed = discord.Embed(description=message, color=0xABCDEF)
        embed.set_author(name=f'{ctx.author.name} from BRG Official', icon_url=ctx.author.avatar_url)
        await recipient.send(embed=embed)
    else:
        embed = discord.Embed(description='That user is not in BRG Official.', color=0xABCDEF)
        ctx.send(embed=embed)

@bot.command()
async def about(ctx):
    embed = discord.Embed(title='**About BRG Bot**', description='BRG Bot is a custom made Discord bot for the BRG Official Discord server. It was made by **Math Development (obvMath#0289)**.', color=0xABCDEF)
    embed.add_field(name='‏', value='You can learn more about Math Development [here](https://mathdev.page.link/BRG). If you apply for a custom Discord bot from Math Development, use referral code `BRG`.')
    await ctx.reply(embed=embed)

@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send(f'You can use that again in **{round(error.retry_after, 2)}** seconds.')
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.send('You do not have permission to do that.')
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send(f'You are missing the argument **{error.param}**')
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f'That command does not exsist.')

bot.run('TOKEN')
