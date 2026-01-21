#################################################
#This library is just for MGPT2 Trainer function#
#################################################

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

train_dataset = MenuDataset(tokenizer, trainer_texts)   #Train dataset
eval_dataset = MenuDataset(tokenizer, eval_texts)       #eval dataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_DIR = "/app/results"


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