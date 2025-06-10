# Use Case 2: NLP Text Classification

This use case demonstrates a typical NLP text classification workflow using spaCy and HuggingFace Transformers. It covers:

- Text preprocessing and tokenization
- Model training and evaluation
- Comparison of frameworks
- Containerized setup for reproducibility

## Workflow
1. **Data Loading**: Loads a subset of the AG News dataset for multi-class text classification.
2. **spaCy Pipeline**: Uses a simple CNN-based text classifier with spaCy, including custom label setup and training loop.
3. **HuggingFace Transformers**: Fine-tunes DistilBERT for text classification using the Trainer API.
4. **Evaluation**: Reports accuracy for both frameworks.

## Code Highlights
- Demonstrates both traditional (spaCy) and transformer-based (HuggingFace) NLP pipelines.
- Uses the same train/test split for fair comparison.
- Minimal, interview-ready code with clear comments.

## Practical Tips
- Use pre-trained models (e.g., DistilBERT) for strong baselines in NLP tasks.
- For small datasets, limit epochs and use smaller models to avoid overfitting.
- Use Docker for reproducibility: `docker build -t nlp-text-class . && docker run -it nlp-text-class`.

---
See `code/nlp_text_classification_example.py` for the full implementation.

## Contents
- `code/` — Scripts and notebooks
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization
- `interview_qa.md` — Interview Q&A 