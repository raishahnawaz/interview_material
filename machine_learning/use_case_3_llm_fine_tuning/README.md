# Use Case 3: LLM Fine-tuning (HuggingFace Transformers)

This use case demonstrates fine-tuning a pre-trained Large Language Model (LLM) such as DistilBERT on a custom text classification task using HuggingFace Transformers. It covers:

- Preparing data for LLM fine-tuning
- Fine-tuning a pre-trained model
- Model evaluation and comparison
- Containerized setup for reproducibility

## Workflow
1. **Data Loading**: Loads a subset of the IMDb dataset for binary sentiment classification.
2. **Tokenization**: Uses a pre-trained tokenizer (DistilBERT) to process text data.
3. **Fine-tuning**: Fine-tunes DistilBERT for sentiment classification using the Trainer API.
4. **Evaluation**: Reports accuracy on the test set.

## Code Highlights
- Uses HuggingFace's Trainer API for efficient fine-tuning and evaluation.
- Demonstrates how to adapt a pre-trained LLM to a new task with minimal code.
- Minimal, interview-ready code with clear comments.

## Practical Tips
- Use smaller models (e.g., DistilBERT) for quick experimentation and limited resources.
- Always use a validation/test split to evaluate generalization.
- Use Docker for reproducibility: `docker build -t llm-fine-tune . && docker run -it llm-fine-tune`.

---
See `code/llm_fine_tuning_example.py` for the full implementation.

## Contents
- `code/` — Scripts and notebooks
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization
- `interview_qa.md` — Interview Q&A 