import twitch, os, discord, asyncio, time, discord.utils, discord.ext.commands.bot, tcd
from discord.ext import tasks, commands

client_secret = (os.environ['TWITCH_BOT_TOKEN'])

# Twitch API and Discord API

client = commands.Bot(command_prefix = '!t ')

helix = twitch.Helix('9922lagd7woskvvil4muehlheqs66n', client_secret)

class Server:
    def __init__(self, gid, over, notl, li):
        self.guild_id = gid
        self.overall = over
        self.not_live = notl
        self.live = li


everything = []



@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!t command for help"))
    print('Bot Started!')
    for guild in client.guilds:
        everything.append(Server(guild.id,[],[],[]))
    

@client.event
async def on_guild_join(guild):
    everything.append(Server(guild.id,[],[],[]))

    if discord.utils.get(guild.roles, name="Twitch Bot Owner") == None:
        await guild.create_role(name="Twitch Bot Owner")

    if (discord.utils.get(guild.text_channels, name="twitch-commands") == None) and (discord.utils.get(guild.text_channels, name="stream") == None):
        await guild.create_text_channel('twitch-commands')

        channel1 = discord.utils.get(guild.text_channels, name="twitch-commands")
        await channel1.send("This channel is used to add and remove people from the streaming list!")
        await channel1.set_permissions(guild.default_role, send_messages=False)

        await guild.create_text_channel('stream')

        channel2 = discord.utils.get(guild.text_channels, name="stream")
        await channel2.set_permissions(guild.default_role, send_messages=False)
        await channel2.send("This channel is used to tell people that someone is streaming!")


    elif (discord.utils.get(guild.text_channels, name="twitch-commands") == None) and (discord.utils.get(guild.text_channels, name="stream") != None):
        await guild.create_text_channel('twitch-commands')

        channel1 = discord.utils.get(guild.text_channels, name="twitch-commands")
        await channel1.set_permissions(guild.default_role, send_messages=False)
        await channel1.send("This channel is used to add and remove people from the streaming list!")

        channel2 = discord.utils.get(guild.text_channels, name="stream")

        await channel2.set_permissions(guild.default_role, send_messages=False)
        await channel2.send("This channel is used to tell people that someone is streaming!")


    elif (discord.utils.get(guild.text_channels, name="twitch-commands") != None) and (discord.utils.get(guild.text_channels, name="stream") == None):
        channel1 = discord.utils.get(guild.text_channels, name="twitch-commands")
        await channel1.send("This channel is used to add and remove people from the streaming list!")
        await channel1.set_permissions(guild.default_role, send_messages=False)

        await guild.create_text_channel('stream')
        channel2 = discord.utils.get(guild.text_channels, name="stream")

        await channel2.set_permissions(guild.default_role, send_messages=False)
        await channel2.send("This channel is used to tell people that someone is streaming!")

    else:
        channel1 = discord.utils.get(guild.text_channels, name="twitch-commands")
        await channel1.send("This channel is used to add and remove people from the streaming list!")
        await channel1.set_permissions(guild.default_role, send_messages=False)

        channel2 = discord.utils.get(guild.text_channels, name="stream")

        await channel2.send("This channel is used to tell people that someone is streaming!")
        await channel2.set_permissions(guild.default_role, send_messages=False)

@client.event
async def on_guild_remove(guild):
    x = len(everything)
    for i in range(x):
        if everything[i].guild_id == guild.id:
            everything.pop(i)
            break

# TESTING DONE (TESTED MORE)

async def search():
    await client.wait_until_ready()
    while True:
        x = len(everything)

        try:
            for i in range(x):
                guild = everything[i].guild_id
                name = (client.get_guild(guild))
                channel = discord.utils.get(name.text_channels, name="stream")
                if channel != None:
                    for user in helix.users(everything[i].overall):
                        print(everything[i].guild_id)
                        print(everything[i].live)
                        print(everything[i].not_live)
                        print(everything[i].overall)
                        print(user.is_live)
                        if ((user.data.get('display_name') in everything[i].not_live) == True) and (user.is_live == True):
                            everything[i].not_live.remove(user.data.get('display_name'))
                            everything[i].live.append(user.data.get('display_name'))

                            print(everything[i].guild_id)
                            print(everything[i].live)
                            print(everything[i].not_live)
                            print(everything[i].overall)
                            print(user.is_live)

                            embed = discord.Embed(title=str(user.stream), color=0x6441a4)
                            embed.set_author(name=user.data.get('login'), url= 'https://www.twitch.tv/' + user.data.get('login')
                                        , icon_url= user.data.get('profile_image_url'))
                            embed.set_thumbnail(url = user.data.get('profile_image_url'))
                            embed.add_field(name="*Game*", value=user.stream.data.get('game_name'))
                            embed.add_field(name="*Viewers*", value=user.stream.data.get('viewer_count'))
                            embed.set_image(url= 'https://static-cdn.jtvnw.net/previews-ttv/live_user_' + 
                                        user.stream.data.get('user_login') + '-320x180.jpg')
                            embed.set_footer(text= "Made By: @RabbiT Cause MEE6 SUCKS")
                            await channel.send("Hey @everyone, " + user.display_name + " is now live on " +
                                         "<https://www.twitch.tv/" + user.data.get('login') +"> ! Go check it out!")

                            await channel.send(embed=embed)
                        elif (user.data.get('display_name') in everything[i].live) == True and (user.is_live == False):
                            everything[i].not_live.append(user.data.get('display_name'))
                            everything[i].live.remove(user.data.get('display_name'))
                else:
                    pass
        except Exception:
            pass

        await asyncio.sleep(60) #change to 30 seconds at final
    await search()

    

#TESTING DONE

@client.command()
async def command(ctx):
    embed = discord.Embed(title="Twitch Bot Commands", color=0x6441a4)
    embed.set_author(name="Twitch Bot", icon_url="https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2019/09/03-glitch.jpg?w=496&h=331&quality=82&strip=all&ssl=1")
    embed.add_field(name="*First Time Look*", value="___", inline=False)
    embed.add_field(name="TWITCH-COMMANDS CHANNEL", value="This is where you put the put the add and remove. If removed, bot will not work. :)", inline=False)
    embed.add_field(name="STREAM CHANNEL", value="This is where the people that just started streaming will go live. If removed, bot will not work. :)", inline=False)
    embed.add_field(name="TWITCH-BOT-OWNER ROLE", value="This role is how people can get added to the list of streamers. If removed, bot will not work. :)", inline=False)

    
    embed.add_field(name="*Commands*", value="___", inline=False)
    embed.add_field(name="!t add (streamer)  EX: !t add shroud ( ONLY FOR TWITCH BOT OWNER )", value="Adds a streamer to the list", inline=False)

    embed.add_field(name="!t remove (streamer)  EX: !t remove shroud ( ONLY FOR TWITCH BOT OWNER )", value="Removes a streamer to the list", inline=False)

    embed.add_field(name="!t printList", value="Prints the list of streamers that are added!", inline=False)

    embed.add_field(name="!t printLiveList", value="Prints the list of streamers that are live!", inline=False)

    embed.add_field(name="!t printNotLiveList", value="Prints the list of streamers that are not live!", inline=False)

    embed.set_footer(text= "Made by: @RabbiT")
    await ctx.channel.send(embed=embed)
    return


# TESTING DONE (TESTED MORE)

@client.command()
@commands.has_role('Twitch Bot Owner')
async def add(ctx, arg):
    
    x = len(everything)

    for i in range(x):
        if everything[i].guild_id == ctx.message.guild.id:
            ind = i
            break


    if str(ctx.channel) == 'twitch-commands':
        author = ctx.message.author.mention
        try:
            user = helix.user(arg)
            user = user.data.get('display_name')
            if user in everything[i].overall:
                await ctx.channel.send("Streamer Already Added! " + author)
            else:
                everything[i].not_live.append(user)
                everything[i].overall.append(user)
                await ctx.channel.send("Done " + author)

        except Exception:
           await ctx.channel.send("Streamer NOT Valid " + author)


# TESTING DONE (TESTED MORE)

@client.command()
@commands.has_role('Twitch Bot Owner')
async def remove(ctx, arg):

    x = len(everything)

    for i in range(x):
        if everything[i].guild_id == ctx.message.guild.id:
            ind = i
            break

    if str(ctx.channel) == 'twitch-commands':
        author = ctx.message.author.mention
        try:
            user = helix.user(arg)
            user = user.data.get('display_name')
            if user in everything[i].overall:
                everything[i].overall.remove(user)

                if user in everything[i].not_live:
                    everything[i].not_live.remove(user)
                else:
                    everything[i].live.remove(user)
                
                await ctx.channel.send("Done " + author)
            else:
                await ctx.channel.send("Streamer NOT Found " + author)

        except Exception:
            await ctx.channel.send("Streamer NOT Found")


# TESTING DONE (TESTED MORE)

@client.command()
async def printList(ctx):
    x = len(everything)

    for i in range(x):
        if everything[i].guild_id == ctx.message.guild.id:
            ind = i
            break

    embed = discord.Embed(title="List of Streamers", color=0x6441a4)
    embed.set_author(name="Twitch Bot", icon_url="https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2019/09/03-glitch.jpg?w=496&h=331&quality=82&strip=all&ssl=1")
    embed.set_footer(text= "Made by: @RabbiT")
    for user in helix.users(everything[i].overall):
        embed.add_field(name=":purple_circle: " + user.display_name , value="**Description:** \n" + user.data.get('description') 
                            + "\n" + "**Link:** \nhttps://www.twitch.tv/" + user.data.get('login')  + "\n____", inline=False)

    await ctx.channel.send(embed=embed)
    return

# TEST DONE (TESTED MORE)

@client.command()
async def printLiveList(ctx):
    x = len(everything)

    for i in range(x):
        if everything[i].guild_id == ctx.message.guild.id:
            ind = i
            break

    embed = discord.Embed(title="List of Streamers", color=0x6441a4)
    embed.set_author(name="Twitch Bot", icon_url="https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2019/09/03-glitch.jpg?w=496&h=331&quality=82&strip=all&ssl=1")
    embed.set_footer(text= "Made by: @RabbiT")
    for user in helix.users(everything[i].live):
        embed.add_field(name=":purple_circle: " + user.display_name , value="**Description:** \n" + user.data.get('description') 
                            + "\n" + "**Link:** \nhttps://www.twitch.tv/" + user.data.get('login')  + "\n____", inline=False)

    await ctx.channel.send(embed=embed)
    return

# TEST DONE (TESTED MORE)

@client.command()
async def printNotLiveList(ctx):
    x = len(everything)

    for i in range(x):
        if everything[i].guild_id == ctx.message.guild.id:
            ind = i
            break

    embed = discord.Embed(title="List of Streamers", color=0x6441a4)
    embed.set_author(name="Twitch Bot", icon_url="https://i0.wp.com/9to5mac.com/wp-content/uploads/sites/6/2019/09/03-glitch.jpg?w=496&h=331&quality=82&strip=all&ssl=1")
    embed.set_footer(text= "Made by: @RabbiT")
    for user in helix.users(everything[i].not_live):
        embed.add_field(name=":purple_circle: " + user.display_name , value="**Description:** \n" + user.data.get('description') 
                            + "\n" + "**Link:** \nhttps://www.twitch.tv/" + user.data.get('login')  + "\n____", inline=False)

    await ctx.channel.send(embed=embed)
    return



client.loop.create_task(search())
client.run(os.environ['TWITCH_BOT_DISCORD_TOKEN'])

