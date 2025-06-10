"""
NLP Summarization Example: HuggingFace Transformers (T5)
This script demonstrates abstractive summarization using a pre-trained T5 model on the CNN/DailyMail dataset.
"""

from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.metrics import accuracy_score
import numpy as np

# --- 1. Data Loading ---
print("Loading CNN/DailyMail dataset...")
dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:20]")  # Use a small subset for demo
articles = dataset["article"]
references = dataset["highlights"]

# --- 2. Load Pre-trained T5 Model ---
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# --- 3. Summarization ---
def generate_summary(text):
    input_ids = tokenizer("summarize: " + text, return_tensors="pt", max_length=512, truncation=True).input_ids
    output_ids = model.generate(input_ids, max_length=60, num_beams=2, early_stopping=True)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("\nGenerating summaries...")
pred_summaries = [generate_summary(article) for article in articles]

# --- 4. Simple Evaluation (ROUGE would be better, but use string overlap for demo) ---
def simple_overlap(pred, ref):
    pred_set = set(pred.lower().split())
    ref_set = set(ref.lower().split())
    return len(pred_set & ref_set) / max(1, len(ref_set))

overlaps = [simple_overlap(pred, ref) for pred, ref in zip(pred_summaries, references)]
print(f"\nAverage word overlap with reference summaries: {np.mean(overlaps):.2f}")

# Print a few examples
for i in range(3):
    print(f"\nArticle: {articles[i][:200]}...")
    print(f"Reference Summary: {references[i]}")
    print(f"Predicted Summary: {pred_summaries[i]}")

print("\nT5 summarization complete on CNN/DailyMail subset.") 