#official library
import mariadb, dotenv, os, random
#MintyBot library
from src import MintyBot

#load environment
dotenv.load_dotenv()

##########################################################################################
# this module doesn't need execute or fetchone, because of initialization for channel_id #
##########################################################################################

client = MintyBot.client

@client.command()
async def hello(ctx):
    await ctx.send(f"Hello! I'm MintyBot! Anything you needed, type {os.getenv('COMMAND_PREFIX','+')}help")

@client.command()
async def ping(ctx):
    await ctx.send('pong!')

@client.command()
async def dice(ctx):
        a = random.randrange(1,7)
        b = random.randrange(1,7)

        if a > b:
            await ctx.send("패배")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a == b:
            await ctx.send("무승부")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))
        elif a < b:
            await ctx.send("승리")
            await ctx.send("봇의 숫자: " + str(a) + " 당신의 숫자: " +  str(b))

@client.command()
async def mintyhelp(ctx):
     await ctx.send("아직 준비중입니다.")


#this function is for debugging discord.py's problems. 

@client.command()
async def guildtestcode(ctx):
     
    await ctx.send("[MintyDev] Gathering guild information...")
    print(f"[MintyDev] Guild ID: {ctx.guild.id if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Guild Name: {ctx.guild.name if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Is Command Invoked in a Guild: {ctx.guild is not None}")
    print(f"[MintyDev] Guild Member Count: {ctx.guild.member_count if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Is Author the Guild Owner: {ctx.guild is not None and ctx.author.id == ctx.guild.owner_id}")
    print(f"[MintyDev] Guild Region: {ctx.guild.region if ctx.guild and hasattr(ctx.guild, 'region') else 'N/A'}")
    print(f"[MintyDev] Guild Verification Level: {ctx.guild.verification_level if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Boost Level: {ctx.guild.premium_tier if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Boost Count: {ctx.guild.premium_subscription_count if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Owner ID: {ctx.guild.owner_id if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Created At: {ctx.guild.created_at if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Description: {ctx.guild.description if ctx.guild and ctx.guild.description else 'N/A'}")
    print(f"[MintyDev] Guild Vanity URL: {ctx.guild.vanity_url_code if ctx.guild and ctx.guild.vanity_url_code else 'N/A'}")
    print(f"[MintyDev] Guild Features: {ctx.guild.features if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild AFK Channel: {ctx.guild.afk_channel.name if ctx.guild and ctx.guild.afk_channel else 'N/A'}")
    print(f"[MintyDev] Guild AFK Timeout: {ctx.guild.afk_timeout if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild System Channel: {ctx.guild.system_channel.name if ctx.guild and ctx.guild.system_channel else 'N/A'}")
    print(f"[MintyDev] Guild Rules Channel: {ctx.guild.rules_channel.name if ctx.guild and ctx.guild.rules_channel else 'N/A'}")
    print(f"[MintyDev] Guild Public Updates Channel: {ctx.guild.public_updates_channel.name if ctx.guild and ctx.guild.public_updates_channel else 'N/A'}")
    print(f"[MintyDev] Guild Maximum Members: {ctx.guild.max_members if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Maximum Presences: {ctx.guild.max_presences if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Emoji Count: {len(ctx.guild.emojis) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Sticker Count: {len(ctx.guild.stickers) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Is Guild Verified: {ctx.guild.verified if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Partnered: {ctx.guild.partnered if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Community: {ctx.guild.community if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Discovery Splash URL: {ctx.guild.discovery_splash.url if ctx.guild and ctx.guild.discovery_splash else 'N/A'}")
    print(f"[MintyDev] Guild Banner URL: {ctx.guild.banner.url if ctx.guild and ctx.guild.banner else 'N/A'}")
    print(f"[MintyDev] Guild Icon URL: {ctx.guild.icon.url if ctx.guild and ctx.guild.icon else 'N/A'}")
    print(f"[MintyDev] Guild Splash URL: {ctx.guild.splash.url if ctx.guild and ctx.guild.splash else 'N/A'}")
    print(f"[MintyDev] Guild Preferred Locale: {ctx.guild.preferred_locale if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Vanity URL Uses: {ctx.guild.vanity_url_uses if ctx.guild and ctx.guild.vanity_url_uses else 'N/A'}")
    print(f"[MintyDev] Guild Welcome Screen: {ctx.guild.welcome_screen.description if ctx.guild and ctx.guild.welcome_screen else 'N/A'}")
    print(f"[MintyDev] Guild Widget Enabled: {ctx.guild.widget_enabled if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Widget Channel: {ctx.guild.widget_channel.name if ctx.guild and ctx.guild.widget_channel else 'N/A'}") 
    print(f"[MintyDev] Guild Large: {ctx.guild.large if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Shard ID: {ctx.guild.shard_id if ctx.guild else 'N/A'}")   
    print(f"[MintyDev] Guild Member Chunk Count: {ctx.guild.chunked if ctx.guild else 'N/A'}")  
    print(f"[MintyDev] Guild Maximum Video Channel Users: {ctx.guild.max_video_channel_users if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Stage Instances Count: {len(ctx.guild.stage_instances) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Scheduled Events Count: {len(ctx.guild.scheduled_events) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Stickers Count: {len(ctx.guild.stickers) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Emojis Count: {len(ctx.guild.emojis) if ctx.guild else 'N/A'}")    
    print(f"[MintyDev] Guild Roles Count: {len(ctx.guild.roles) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Channels Count: {len(ctx.guild.channels) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Voice States Count: {len(ctx.guild.voice_states) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Members Count: {len(ctx.guild.members) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Presences Count: {len(ctx.guild.presences) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Invites Count: {len(await ctx.guild.invites()) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Bans Count: {len(await ctx.guild.bans()) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Audit Logs Count: {len([entry async for entry in ctx.guild.audit_logs(limit=100)]) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Integrations Count: {len(await ctx.guild.integrations()) if ctx.guild else 'N/A'}")
    print(f"[MintyDev] Guild Application Commands Count: {len(await ctx.guild.application_commands()) if ctx.guild else 'N/A'}")
    await ctx.send("[MintyDev] Guild information gathering completed!")

    return


@client.command()
async def testcode(ctx):

    await ctx.send("[MintyDev] This is a test code!")
    print("[MintyDev] Test code executed!")
    print(f"[MintyDev] Command executed by {ctx.author.name} in channel {ctx.channel.name} ({ctx.channel.id})")
    print(f"[MintyDev] Full Message Content: {ctx.message.content}")
    print(f"[MintyDev] Author ID: {ctx.author.id}")
    print(f"[MintyDev] Channel ID: {ctx.channel.id}")
    print(f"[MintyDev] Message ID: {ctx.message.id}")
    print(f"[MintyDev] Timestamp: {ctx.message.created_at}")
    print(f"[MintyDev] Is Author a Bot: {ctx.author.bot}")
    print(f"[MintyDev] Channel Type: {ctx.channel.type}")
    print(f"[MintyDev] Command Prefix Used: {ctx.prefix}")
    print(f"[MintyDev] Command Invoked: {ctx.command}")
    print(f"[MintyDev] Context Args: {ctx.args}")
    print(f"[MintyDev] Context Kwargs: {ctx.kwargs}")
    print(f"[MintyDev] Author Roles: {[role.name for role in ctx.author.roles] if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Channel Permissions for Author: {ctx.channel.permissions_for(ctx.author) if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Is Command Invoked in a DM: {ctx.guild is None}")
    print(f"[MintyDev] Author Display Name: {ctx.author.display_name}")
    print(f"[MintyDev] Channel Mention: {ctx.channel.mention}")
    print(f"[MintyDev] Message Clean Content: {ctx.message.clean_content}")
    print(f"[MintyDev] Message Jump URL: {ctx.message.jump_url}")
    print(f"[MintyDev] Channel Topic: {ctx.channel.topic if hasattr(ctx.channel, 'topic') else 'N/A'}") 
    print(f"[MintyDev] Channel NSFW: {ctx.channel.is_nsfw() if hasattr(ctx.channel, 'is_nsfw') else 'N/A'}")
    print(f"[MintyDev] Author Joined At: {ctx.author.joined_at if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Author Accent Color: {ctx.author.accent_color if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Author Banner URL: {ctx.author.banner.url if ctx.author.banner else 'No Banner'}")
    print(f"[MintyDev] Author Avatar URL: {ctx.author.avatar.url if ctx.author.avatar else 'No Avatar'}")
    print(f"[MintyDev] Is Message Edited: {ctx.message.edited_at is not None}")
    print(f"[MintyDev] Message Edited Timestamp: {ctx.message.edited_at if ctx.message.edited_at else 'Never Edited'}")
    print(f"[MintyDev] Channel Category: {ctx.channel.category.name if ctx.channel.category else 'No Category'}")
    print(f"[MintyDev] Is Author Muted: {ctx.author.voice.muted if ctx.guild and ctx.author.voice else 'N/A'}")
    print(f"[MintyDev] Is Author Deafened: {ctx.author.voice.deafened if ctx.guild and ctx.author.voice else 'N/A'}")
    print(f"[MintyDev] Author Voice Channel: {ctx.author.voice.channel.name if ctx.guild and ctx.author.voice and ctx.author.voice.channel else 'N/A'}")
    print(f"[MintyDev] Author Top Role: {ctx.author.top_role.name if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Channel Slowmode Delay: {ctx.channel.slowmode_delay if hasattr(ctx.channel, 'slowmode_delay') else 'N/A'}")
    print(f"[MintyDev] Is Channel Archived: {ctx.channel.is_archived() if hasattr(ctx.channel, 'is_archived') else 'N/A'}")
    print(f"[MintyDev] Channel Member Count: {ctx.channel.member_count if hasattr(ctx.channel, 'member_count') else 'N/A'}")
    print(f"[MintyDev] Is Author a Nitro Subscriber: {ctx.author.premium_since is not None if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Author Nitro Since: {ctx.author.premium_since if ctx.guild and ctx.author.premium_since else 'N/A'}")
    print(f"[MintyDev] Is Author a Server Booster: {ctx.author.premium_since is not None if ctx.guild else 'Direct Message'}")
    print(f"[MintyDev] Author Server Boost Since: {ctx.author.premium_since if ctx.guild and ctx.author.premium_since else 'N/A'}")
    print(f"[MintyDev] check if user has administrator permission: {ctx.channel.permissions_for(ctx.author).administrator if ctx.guild else 'Direct Message'}")
    
    # You can add more debug information as needed
    await ctx.send("[MintyDev] Test code execution completed!")
    return
