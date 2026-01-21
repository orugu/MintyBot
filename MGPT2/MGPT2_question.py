import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset
from torch.optim import AdamW
import os
import transformers

from MGPT2.MGPT2_lib import trainer_texts, eval_texts, device, BASE_DIR, train_dataset, eval_dataset

transformers.utils.import_utils._torchvision_available = False
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"



# 토크나이저와 모델 로드
tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2', cache_dir="/tmp/hf_cache")
tokenizer.add_special_tokens({'pad_token': '[PAD]'})  # 특수 토큰 추가
model = GPT2LMHeadModel.from_pretrained('distilgpt2', cache_dir="/tmp/huggingface")   #사전 학습된 모델 입력
# 토큰 임베딩 크기 재조정
model.resize_token_embeddings(len(tokenizer))

optimizer = AdamW(model.parameters(), lr=5e-5)   #최적화



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
    
