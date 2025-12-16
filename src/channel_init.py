#official library
import mariadb

#MintyBot library
from src import MintyBot

#MintyCurrency library
from lib.sqlalchemy_lib import engine, crud

##########################################################################################
# this module doesn't need execute or fetchone, because of initialization for channel_id #
##########################################################################################

client = MintyBot.client

@client.command()
async def initialize(ctx): 
    print(f"""[MintyBot Initialize] Initialize Started
          guild name:{ctx.guild.name}
          channel name : {ctx.channel.name}""")
    try:

        MintyBot.MintyBot_cur.execute("INSERT INTO serverinfo (channel_id) VALUES (?)", (ctx.channel.id,))
        MintyBot.MintyBot_conn.commit()
        await ctx.send("completed initialization for Mintybot in this channel.")
        print("[MintyBot Initialize] Initialize Completed")
        
    except mariadb.Error as e:
        await ctx.send(f"Initialization failed: {e}")
        print(f"[MintyBot Initialize] Initialize Failed: {e}")

    db = engine.SessionLocal()

    try:
        ok = crud.add_channel(db, ctx.channel.id)
        if ok:
            await ctx.send("Initialization completed.")
        else:
            await ctx.send("Already initialized.")
    finally:
        db.close()
            

@client.command()
async def deinitialize(ctx):
    print("[MintyBot Deinitialize] Deinitialize Started")
    try:
        MintyBot.MintyBot_cur.execute("DELETE FROM serverinfo WHERE channel_id = ?", (ctx.channel.id,))
        MintyBot.MintyBot_conn.commit()
        await ctx.send("completed deinitialization for Mintybot in this channel.")
        print("[MintyBot Deinitialize] Deinitialize Completed")
    except mariadb.Error as e:
        await ctx.send(f"Deinitialization failed: {e}")
    
    db = engine.SessionLocal()
    try:
        ok = crud.remove_channel(db, ctx.channel.id)
        if ok:
            await ctx.send("Deinitialized.")
        else:
            await ctx.send("Not initialized.")
    finally:
        db.close()