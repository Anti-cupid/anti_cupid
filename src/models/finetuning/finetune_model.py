import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset, Dataset

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

train_data = {}  # To-Do
train_dataset = Dataset.from_dict(train_data)


def tokenize_function(examples):
    inputs = [
        ex + " " + tokenizer.sep_token + " " + out
        for ex, out in zip(examples["input"], examples["output"])
    ]
    model_inputs = tokenizer(
        inputs, max_length=512, truncation=True, padding="max_length"
    )
    return model_inputs


tokenized_datasets = train_dataset.map(tokenize_function, batched=True)
tokenized_datasets.set_format(type="torch", columns=["input_ids", "attention_mask"])

training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=3,
    save_steps=500,
    warmup_steps=100,
    gradient_accumulation_steps=8,
    fp16=True if torch.cuda.is_available() else False,
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
