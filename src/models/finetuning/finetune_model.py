from collections import defaultdict
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    Trainer,
    TrainingArguments,
    pipeline,
)
from datasets import load_dataset, Dataset
import json


def setup_ddp():
    # DDP Settings
    torch.distributed.init_process_group(backend="nccl")


def get_device(rank):
    # Set the device for process
    if torch.cuda.is_available():
        torch.cuda.set_device(rank)
        return torch.device(f"cuda:{rank}")
    else:
        return torch.device("cpu")


model_name = "MLP-KTLim/llama-3-Korean-Bllossom-8B"

# model = pipeline(
#     "text-generation",
#     model=model_name,
#     model_kwargs={"torch_dtype": torch.bfloat16},
#     device_map="auto",
# )

model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16)
tokenizer = AutoTokenizer.from_pretrained(model_name)

setup_ddp()
rank = torch.distributed.get_rank()
device = get_device(rank)
model.to(device)
model = torch.nn.parallel.DistributedDataParallel(
    model, device_ids=[torch.cuda.current_device()]
)

# if torch.distributed.get_rank() == 0:
#     pass

with open("../../../data/data_2023.json", "r", encoding="utf-8") as f:
    data = json.load(f)

examples = []
for entry in data:
    if entry["이유"] and entry["주문"]:
        input_text = entry["이유"]
        target_text = entry["주문"]
        examples.append({"input_text": input_text, "target_text": target_text})

data_dict = defaultdict(list)
for example in examples:
    for key, value in example.items():
        data_dict[key].append(value)

dataset = Dataset.from_dict(data_dict)


def tokenize_function(batch):
    PROMPT = """You are a helpful AI assistant. Please answer the user's questions kindly. 당신은 유능한 AI 어시스턴트 입니다. 사용자의 질문에 대해 친절하게 답변해주세요."""

    inputs = []
    targets = []
    for user_message, assistant_reply in zip(batch["input_text"], batch["target_text"]):
        messages = [
            {"role": "system", "content": f"{PROMPT}"},
            {"role": "user", "content": user_message},
        ]

        prompt = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )

        inputs.append(prompt)
        targets.append(assistant_reply)

    # Tokenize the inputs and targets
    model_inputs = tokenizer(
        inputs, max_length=128, truncation=True, padding="max_length"
    )

    # Tokenize the targets using the target tokenizer context
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(
            targets, max_length=64, truncation=True, padding="max_length"
        )

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs


training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    warmup_steps=100,
    gradient_accumulation_steps=16,
    fp16=True,
    load_best_model_at_end=True,
    metric_for_best_model="loss",
)

tokenized_datasets = dataset.map(
    tokenize_function, batched=True, remove_columns=["input_text", "target_text"]
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    tokenizer=tokenizer,
)

trainer.train()

trainer.save_model("./finetuned_model")
tokenizer.save_pretrained("./finetuned_model")
