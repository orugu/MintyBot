import sys, mariadb
import os
from dotenv import load_dotenv

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

# -----------------------------------
# Connect to MariaDB
# -----------------------------------

def get_server_db():
    try:
        channel_enable_list = mariadb.connect(
            host= os.getenv("MINTYBOT_DB_HOST", "localhost"),
            user= os.getenv("MINTYBOT_DB_USER", "username"),
            password= os.getenv("MINTYBOT_DB_PASSWORD", "password"),
            database= os.getenv("MINTYBOT_DB_DATABASE", "mintybot"),
            port= int(os.getenv("MINTYBOT_DB_PORT", 53305)))
        return channel_enable_list
    
    except mariadb.Error as e:
        print(f"[DB ERROR] Database Connection Failed: {e}")
        sys.exit(1)
