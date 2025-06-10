"""
LLM Fine-tuning Example: HuggingFace Transformers (DistilBERT)
This script demonstrates fine-tuning a pre-trained DistilBERT model on the IMDb sentiment classification task.
"""

import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

# --- 1. Data Loading ---
print("Loading IMDb dataset...")
dataset = load_dataset("imdb", split="train[:2000]")  # Use a small subset for demo
texts = dataset["text"]
labels = dataset["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# --- 2. Tokenization ---
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=256)

train_df = pd.DataFrame({"text": X_train, "label": y_train})
test_df = pd.DataFrame({"text": X_test, "label": y_test})

train_dataset = load_dataset("csv", data_files={"train": train_df.to_csv(index=False)}, split="train")
test_dataset = load_dataset("csv", data_files={"test": test_df.to_csv(index=False)}, split="test")

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

# --- 3. Model & Training ---
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=1,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    logging_steps=10,
    disable_tqdm=True,
    logging_dir="./logs",
    save_strategy="no"
)

def compute_metrics(p):
    preds = p.predictions.argmax(axis=1)
    return {"accuracy": (preds == p.label_ids).mean()}

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=compute_metrics
)

trainer.train()
results = trainer.evaluate()
print(f"DistilBERT IMDb Fine-tuning Accuracy: {results['eval_accuracy']:.4f}")

print("\nDistilBERT fine-tuned and evaluated on IMDb sentiment classification subset.") 