import sys, mariadb
import os, discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
from src.MintyHelp import HelpCommands
# -----------------------------------
# .env config load
# add to .env
#
# MINTYBOT_DB_HOST="your ip or address"
# MINTYBOT_DB_PORT="your port"
# MINTYBOT_DB_USER="your user"
# MINTYBOT_DB_PASSWORD="your password"
# MINTYBOT_DB_DATABASE="your database"
# -----------------------------------



load_dotenv()

client = commands.Bot(command_prefix="!",intents=discord.Intents.all(), help_command=HelpCommands())
voiceclient=discord.utils.get(client.voice_clients,guild=client.guilds)

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

_MintyBot_conn = None

def get_db():
    """
    Docstring for get_db

    :return: Description
    :rtype: mariadb.Connection  
    """
    global _MintyBot_conn

    if _MintyBot_conn is None:
        print("[MintyBot] Main DB Connection started")
        _MintyBot_conn = mariadb.connect(
            host=os.getenv("MINTYBOT_DB_HOST", "localhost"),
            user=os.getenv("MINTYBOT_DB_USER", "username"),
            password=os.getenv("MINTYBOT_DB_PASSWORD", "password"),
            database=os.getenv("MINTYBOT_DB_DATABASE", "mintybot"),
            port=int(os.getenv("MINTYBOT_DB_PORT", 53305)),
            autocommit=False
        )
        print("[MintyBot] Main DB Connection Completed")

    return _MintyBot_conn


def get_cursor():
    return get_db().cursor()

def is_channel_enabled(channel_id: int) -> bool:
    """
    Docstring for is_channel_enabled
    
    :param channel_id: Description
    :type channel_id: int
    :return: Description
    :rtype: bool
    """
    cur = get_cursor()
    try:
        cur.execute(
            "SELECT EXISTS(SELECT 1 FROM serverinfo WHERE channel_id = ?)",
            (channel_id,)
        )
        return cur.fetchone()[0] == 1
    finally:
        cur.close()

def is_admin_permisson(ctx) -> bool:
    """
    Docstring for is_admin_permisson

    :param ctx: Description
    :return: Description
    :rtype: bool
    """
    result = ctx.channel.permissions_for(ctx.author).administrator if ctx.guild else 'Direct Message'
    return result