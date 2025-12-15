from MintyGPT2 import MGPT2
import os
from config import minty_env

async def initialize()->None:
    """
    for MGPT2 library initialization
    """
    #test code
    MGPT_Load_Flag= minty_env("MGPT2_ENABLE")
    
    print(f"[MGPT2] this is Test code for other modules. MGPT2 unloaded")
    
    if MGPT_Load_Flag == False:

        await MGPT2.load_full_model()
        MGPT_Load_Flag = True
    else:
        print("[MGPT2] distilGPT2 already loaded")
