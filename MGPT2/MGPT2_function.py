from MintyGPT2 import MGPT2
import os
from config import minty_env
from dotenv import load_dotenv

load_dotenv()

async def initialize()->None:
    """
    for MGPT2 library initialization
    """
    #test code
    MGPT_Load_Flag= os.getenv("MGPT2_Enable")
    
    print(f"[MGPT2] this is Test code for other modules. MGPT2 unloaded")
    
    if MGPT_Load_Flag == False:

        await MGPT2.load_full_model()
        MGPT_Load_Flag = True
    else:
        print("[MGPT2] distilGPT2 already loaded")
