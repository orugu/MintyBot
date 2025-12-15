import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset
from torch.optim import AdamW
import os
import transformers

transformers.utils.import_utils._torchvision_available = False
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = "/app/results"
class MenuDataset(Dataset):
    def __init__(self, tokenizer, texts, max_length=128):
        self.tokenizer = tokenizer
        self.inputs = []
        self.attn_masks = []
        self.labels = []
        self.device= device
        for text in texts:
            encodings_dict = tokenizer(text, truncation=True, max_length=max_length, padding="max_length")
            self.inputs.append(torch.tensor(encodings_dict['input_ids']))
            self.attn_masks.append(torch.tensor(encodings_dict['attention_mask']))
            self.labels.append(torch.tensor(encodings_dict['input_ids']))  # labels are the same as input_ids for LM

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return {
            'input_ids': self.inputs[idx],
            'attention_mask': self.attn_masks[idx],
            'labels': self.labels[idx]  # ensure labels are returned
        }



trainer_texts = [
    "User: Show me the menu. Waiter: Here's the menu: hamburger, cola.",
    "User: What is the ESP32? AI: ESP32 is a board for IoT devices.",
    "User: How does a DC motor work? AI: It converts electrical energy into rotational motion using magnetic fields.",
    "User: What's the difference between AI and ML? AI: Machine Learning is a subset of Artificial Intelligence focused on learning from data.",
    "User: Explain Ohm's Law. AI: Ohm's Law states that V = I * R, where voltage equals current times resistance.",
    "User: What is Docker? AI: Docker is a platform that allows you to package applications into containers for easy deployment.",
    "User: How do I install Python packages? AI: Use 'pip install <package_name>' in your terminal.",
    "User: Tell me about GPU acceleration. AI: GPU acceleration speeds up computation by using parallel processing on a graphics processor.",
    "User: What is a REST API? AI: A REST API uses HTTP requests to access and manipulate resources in a stateless manner.",
    "User: What's the meaning of IoT? AI: IoT stands for Internet of Things, connecting physical devices to the internet for data exchange."
]

# 토크나이저와 모델 로드
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2', cache_dir="/tmp/hf_cache")
tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # 특수 토큰 추가
model = GPT2LMHeadModel.from_pretrained('distilgpt2', cache_dir="/tmp/huggingface")   #사전 학습된 모델 입력
# 토큰 임베딩 크기 재조정
model.resize_token_embeddings(len(tokenizer))

optimizer = AdamW(model.parameters(), lr=5e-5)   #최적화
eval_texts = [
    "User: How do I use GPT-2? AI: GPT-2 can be used for text generation tasks.",
    "User: Can you tell me a joke? AI: Why did the chicken join a band? Because it had the drumsticks!",
    "User: What is cloud computing? AI: It's the on-demand delivery of computing resources over the internet.",
    "User: Explain what an API key is. AI: An API key is a unique identifier used to authenticate requests to an API.",
    "User: What's the use of ESP32 Wi-Fi? AI: It enables wireless communication for IoT applications.",
    "User: How do I train a model? AI: You feed it data and optimize it using algorithms like gradient descent.",
    "User: What is JSON? AI: JSON is a lightweight data format used for data exchange between systems.",
    "User: How do I debug Python code? AI: You can use print statements or the 'pdb' debugger to step through your code.",
    "User: How does a neural network learn? AI: It adjusts its internal weights based on the error between predicted and actual outputs.",
    "User: What's a container image? AI: It's a portable, standalone package containing everything needed to run software."
]
train_dataset = MenuDataset(tokenizer, trainer_texts)   #Menu dataset
eval_dataset = MenuDataset(tokenizer, eval_texts)
training_args = TrainingArguments(
    output_dir=BASE_DIR,
    overwrite_output_dir=True,          
    num_train_epochs=100,              
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    warmup_steps=100,               
    weight_decay=0.1,               
    logging_dir='./logs',            
    logging_steps=50,               
    do_train=True,                   
    do_eval=True,                    
    gradient_accumulation_steps=64,  
    run_name="ProBert-BFD-MS",       
    seed=3,
    save_total_limit=1,
    fp16=True
    
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    optimizers=(optimizer, None),
    
)

# 학습 시작
def load_quest_model():
    if torch.cuda.is_available():
        MenuDataset.device = torch.device("cuda")  # GPU 사용
        print("Using GPU:", torch.cuda.get_device_name(0))
    else:
        MenuDataset.device = torch.device("cpu")   # CPU 사용
        print("Using CPU")

    trainer.train()
    print("GPT2 질의응답 모델이 성공적으로 로드되었습니다.")



# 학습된 모델로 질문에 답변

async def quest_handle_message(message, prompt):
    

    # 입력을 토크나이저로 처리

    inputs = tokenizer(prompt, return_tensors='pt').to(device)
    
    # 답변 생성
    outputs = model.generate(
        inputs['input_ids'],
        max_length=50,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        pad_token_id=tokenizer.pad_token_id,  # PAD 토큰 ID 사용
        temperature=0.7,
        top_k=50,
        top_p=0.3,
        do_sample=True
    )

    # 생성된 출력을 텍스트로 디코드
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # 인코딩 문제를 해결하기 위해 UTF-8을 명시적으로 사용
    #print(answer.encode('utf-8').decode('utf-8'))
    printtext=answer.replace(prompt,"")
    await message.channel.send(printtext)
    
