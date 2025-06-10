"""
Simple RAG Example: HuggingFace Transformers
This script demonstrates a retrieval-augmented generation pipeline for document QA using HuggingFace's RAG pipeline.
"""

from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch

# Sample knowledge base (small for demo)
documents = [
    "The Eiffel Tower is located in Paris.",
    "The Great Wall of China is visible from space.",
    "Python is a popular programming language.",
    "The capital of Italy is Rome."
]

# 1. Setup tokenizer, retriever, and model
model_name = "facebook/rag-sequence-nq"
tokenizer = RagTokenizer.from_pretrained(model_name)
retriever = RagRetriever.from_pretrained(
    model_name,
    index_name="custom",
    passages=[{"title": f"Doc {i}", "text": doc} for i, doc in enumerate(documents)]
)
model = RagSequenceForGeneration.from_pretrained(model_name)

# 2. User question
question = "Where is the Eiffel Tower?"
inputs = tokenizer(question, return_tensors="pt")

# 3. Generate answer
with torch.no_grad():
    generated = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        num_beams=2,
        min_length=2,
        max_length=32
    )
answer = tokenizer.batch_decode(generated, skip_special_tokens=True)[0]

print(f"Question: {question}")
print(f"Answer: {answer}")

# 4. Show retrieved docs
retrieved_docs = retriever(input_ids=inputs["input_ids"].numpy(), question=question)["docs"]
print("\nTop retrieved documents:")
for i, doc in enumerate(retrieved_docs[0][:2]):
    print(f"Doc {i+1}: {doc['text']}") 