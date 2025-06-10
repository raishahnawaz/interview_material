# Use Case 7: MLOps (CI/CD & Best Practices)

This use case demonstrates MLOps concepts such as CI/CD for model training and deployment, reproducibility, and best practices. It covers:

- Example CI/CD pipeline (e.g., GitHub Actions or Makefile)
- Reproducibility and versioning (e.g., DVC, MLflow)
- Best practices for production ML

## Workflow
1. **Data & Model Versioning**: Use DVC to track datasets and model artifacts, ensuring reproducibility.
2. **Experiment Tracking**: Use MLflow to log parameters, metrics, and models for each experiment.
3. **Automation**: Use a Makefile to automate training, tracking, and artifact management.

## Code Highlights
- Shows DVC commands for data/model versioning and remote storage.
- Demonstrates MLflow logging in a training script.
- Provides a sample Makefile for automation.

## Practical Tips
- Use DVC for reproducible data/model pipelines and remote storage.
- Use MLflow to compare experiments and track model performance.
- Use automation (Makefile, CI/CD) to ensure consistency and reduce manual errors.

---
See `code/mlops_example.md` for the full workflow and code snippets.

## Contents
- `code/` — Scripts and pipeline configs
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization (if needed)
- `interview_qa.md` — Interview Q&A 