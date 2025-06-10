"""
NLP Text Classification Example: spaCy and HuggingFace Transformers
This script demonstrates text preprocessing, model training, and evaluation using the AG News dataset.
"""

import pandas as pd
from datasets import load_dataset
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# --- 1. Data Loading ---
print("Loading AG News dataset...")
dataset = load_dataset("ag_news", split="train[:2000]")  # Use a small subset for demo
texts = dataset["text"]
labels = dataset["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# --- 2. spaCy Pipeline ---
print("\n--- spaCy: Text Classification ---")
import spacy
from spacy.util import minibatch
from spacy.training.example import Example

# Prepare data for spaCy
nlp = spacy.blank("en")
textcat = nlp.add_pipe("textcat_multilabel", config={"exclusive_classes": True, "architecture": "simple_cnn"})
for i in set(y_train):
    textcat.add_label(str(i))

train_data = list(zip(X_train, y_train))
train_examples = [Example.from_dict(nlp.make_doc(text), {"cats": {str(i): i == label for i in set(y_train)}}) for text, label in train_data]

# Training loop (short for demo)
optimizer = nlp.begin_training()
for epoch in range(3):
    losses = {}
    batches = minibatch(train_examples, size=8)
    for batch in batches:
        nlp.update(batch, losses=losses)
    print(f"spaCy Epoch {epoch+1}, Loss: {losses['textcat_multilabel']:.4f}")

# Evaluation
preds = []
for doc in nlp.pipe(X_test):
    pred_label = max(doc.cats, key=doc.cats.get)
    preds.append(int(pred_label))
spacy_acc = accuracy_score(y_test, preds)
print(f"spaCy Accuracy: {spacy_acc:.4f}")

# --- 3. HuggingFace Transformers Pipeline ---
print("\n--- HuggingFace Transformers: DistilBERT ---")
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
import torch

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenize data
def tokenize(batch):
    return tokenizer(batch["text"], padding=True, truncation=True, max_length=128)

train_df = pd.DataFrame({"text": X_train, "label": y_train})
test_df = pd.DataFrame({"text": X_test, "label": y_test})

train_dataset = load_dataset("csv", data_files={"train": train_df.to_csv(index=False)}, split="train")
test_dataset = load_dataset("csv", data_files={"test": test_df.to_csv(index=False)}, split="test")

train_dataset = train_dataset.map(tokenize, batched=True)
test_dataset = test_dataset.map(tokenize, batched=True)

train_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
test_dataset.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=4)

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

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
    compute_metrics=lambda p: {"accuracy": (p.predictions.argmax(axis=1) == p.label_ids).mean()}
)

trainer.train()
results = trainer.evaluate()
print(f"Transformers Accuracy: {results['eval_accuracy']:.4f}")

print("\nBoth spaCy and HuggingFace models trained and evaluated on AG News subset.") 