import sys, mariadb
import os, discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
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

client = commands.Bot(command_prefix="$!",intents=discord.Intents.all())

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

def get_db():
    print("[MintyBot] Main DB Connection started")
    try:
        channel_enable_list = mariadb.connect(
            host= os.getenv("MINTYBOT_DB_HOST", "localhost"),
            user= os.getenv("MINTYBOT_DB_USER", "username"),
            password= os.getenv("MINTYBOT_DB_PASSWORD", "password"),
            database= os.getenv("MINTYBOT_DB_DATABASE", "mintybot"),
            port= int(os.getenv("MINTYBOT_DB_PORT", 53305)))
        print("[MintyBot] Main DB Connection Completed")
        return channel_enable_list
    
    except mariadb.Error as e:
        print(f"[MintyBot] Main DB Connection Failed: {e}")
        sys.exit(1)


MintyBot_conn= get_db()
MintyBot_cur = MintyBot_conn.cursor()
