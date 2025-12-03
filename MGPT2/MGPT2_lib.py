import torch as tc
#from torch.optim import AdamW
#from torch.utils.data import Dataset
from transformers import GPT2LMHeadModel
from transformers import GPT2Tokenizer
from transformers import TrainingArguments
from transformers import pipeline
from transformers import Trainer
import discord, asyncio
from concurrent.futures import ThreadPoolExecutor
import os
from gtts import gTTS
