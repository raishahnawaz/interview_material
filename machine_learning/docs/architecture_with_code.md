# Practical ML/NLP/LLM Architecture: Code Reference Guide

This document maps each use case in this project to the stages of a modern AI/ML workflow, with code references and practical tips. It now includes vision and time series use cases.

---

## How to Use This Guide
- Each workflow stage below is explained in plain language, with links to relevant use cases and code.
- If you're new to ML/NLP, start with the use case READMEs for step-by-step walkthroughs.
- For more on evaluation metrics, see [nlp_evaluation_metrics.md](nlp_evaluation_metrics.md). For NLP history and modeling types, see [nlp_evolution_guide.md](nlp_evolution_guide.md).

---

## Workflow Stages & Use Cases (with Explanations)

1. **Data Processing & Feature Engineering**
   - *What it means:* Cleaning, transforming, and preparing data for modeling. For text, this includes tokenization; for images, normalization; for time series, creating lag features.
   - *Use Case 1: Tabular ML* (see `use_case_1/code/`)
   - *Use Case 2: NLP Text Classification* (see `use_case_2/code/`)
   - *Use Case 8: Vision Classification* (see `use_case_8_vision_classification/code/`)
   - *Use Case 9: Time Series Forecasting* (see `use_case_9_time_series_forecasting/code/`)

2. **Model Training & Fine-tuning**
   - *What it means:* Building models using ML/DL frameworks. Fine-tuning means adapting a pre-trained model to your data.
   - *Use Case 1: Tabular ML* (scikit-learn, TensorFlow, PyTorch)
   - *Use Case 2: NLP Text Classification* (spaCy, HuggingFace Transformers)
   - *Use Case 3: LLM Fine-tuning* (BERT/GPT, see `use_case_3/code/`)
   - *Use Case 8: Vision Classification* (PyTorch CNN)
   - *Use Case 9: Time Series Forecasting* (Prophet)

3. **Model Evaluation**
   - *What it means:* Assessing model performance using metrics (accuracy, F1, ROUGE, ARI, etc.), validation, and explainability.
   - *See each use case's `README.md` and [nlp_evaluation_metrics.md](nlp_evaluation_metrics.md)*

4. **Deployment**
   - *What it means:* Making models available for use (e.g., via REST APIs, batch jobs, or dashboards).
   - *Use Case 5: Model Deployment* (FastAPI/Flask REST API, Docker, Kubernetes)
   - *Use Case 1: Tabular ML* (Streamlit demo)

5. **Monitoring & Feedback**
   - *What it means:* Tracking model performance, detecting drift, collecting user feedback, and retraining as needed.
   - *Use Case 6: Monitoring & Explainability* (drift detection, prediction logging, SHAP, LIME)

6. **MLOps: CI/CD, Versioning, Tracking**
   - *What it means:* Practices and tools for automating, tracking, and governing the ML lifecycle.
   - *Use Case 7: MLOps* (DVC, MLflow, Makefile, automation)

---

## Example: Real Project Flow
1. Collect and preprocess data (tabular, text, images, or time series)
2. Train and evaluate models (try classical ML, deep learning, or transformers)
3. Fine-tune or select the best model
4. Deploy the model as an API or dashboard
5. Monitor performance and collect feedback
6. Use MLOps tools for reproducibility, tracking, and automation
7. Iterate as new data or requirements arise

---

## Practical Tips
- Use Docker for reproducibility and easy deployment.
- Keep requirements minimal and use virtual environments.
- Use open datasets for quick experimentation.
- Reference each use case's `README.md` for detailed walkthroughs.
- Use DVC and MLflow for reproducibility and experiment tracking.
- Monitor models in production for drift and explainability.
- For more on NLP modeling types and history, see [nlp_evolution_guide.md](nlp_evolution_guide.md).
- For evaluation metrics, see [nlp_evaluation_metrics.md](nlp_evaluation_metrics.md).

---

This guide will be updated as new use cases are added and refined. 