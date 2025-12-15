import os

def minty_config()->None:
    """
    this config function must be declared right after os library
    """
    os.makedirs("/tmp/huggingface/xet", exist_ok=True)

    os.environ["TMPDIR"] = "/app/tmp"
    os.environ["TEMP"] = "/app/tmp"
    os.environ["TMP"] = "/app/tmp"
    os.environ["HF_HOME"] = "/tmp/huggingface"
    os.environ["HF_XET_CACHE"] = "/tmp/huggingface/xet"
    os.environ["XDG_CACHE_HOME"] = "/tmp"
    os.environ["TORCH_HOME"] = "/app/torch_cache"

def getenv_bool(input)->bool:
    if os.getenv(input)=="false":
        return False
    elif os.getenv(input)=="true":
        return True
    else:
        return None