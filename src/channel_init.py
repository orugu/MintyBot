#official library
import mariadb

#MintyBot library
from src import MintyBot

##########################################################################################
# this module doesn't need execute or fetchone, because of initialization for channel_id #
##########################################################################################

client = MintyBot.client

@client.command()
async def initialize(ctx): 
    print("[MintyBot Initialize] Initialize Started")
    try:
        MintyBot.MintyBot_cur.execute("INSERT INTO serverinfo (channel_id) VALUES (?)", (ctx.channel.id,))
        MintyBot.MintyBot_conn.commit()
        await ctx.send("completed initialization for Mintybot in this channel.")
        print("[MintyBot Initialize] Initialize Completed")
        
    except mariadb.Error as e:
        await ctx.send(f"Initialization failed: {e}")
        print(f"[MintyBot Initialize] Initialize Failed: {e}")
            

@client.command()
async def deinitialize(ctx):
    try:
        MintyBot.MintyBot_cur.execute("DELETE FROM serverinfo WHERE channel_id = ?", (ctx.channel.id,))
        MintyBot.MintyBot_conn.commit()
        await ctx.send("completed deinitialization for Mintybot in this channel.")
        
    except mariadb.Error as e:
        await ctx.send(f"Deinitialization failed: {e}")
        