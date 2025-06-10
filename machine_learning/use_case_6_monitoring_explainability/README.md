# Use Case 6: Monitoring & Explainability

This use case demonstrates model monitoring (e.g., drift detection, logging) and explainability (e.g., SHAP, LIME) for ML models. It covers:

- Monitoring model predictions and detecting drift
- Explaining model predictions with SHAP or LIME
- Containerized setup for reproducibility

## Workflow
1. **Data Loading & Model Training**: Trains a RandomForestClassifier on the Iris dataset.
2. **Monitoring**: Simulates data drift by shuffling test data and compares accuracy. Logs predictions to CSV for monitoring.
3. **Explainability**:
   - **SHAP**: Generates a summary plot of feature importances.
   - **LIME**: Generates a local explanation for a single prediction and saves it as HTML.

## Code Highlights
- Demonstrates both global (SHAP) and local (LIME) explainability.
- Shows a simple approach to drift detection and prediction logging.
- Minimal, interview-ready code with clear comments.

## Practical Tips
- Use SHAP for global feature importance and LIME for local explanations.
- Monitor model performance over time to detect drift.
- Use Docker for reproducibility: `docker build -t monitoring-explain . && docker run -it monitoring-explain`.

---
See `code/monitoring_explainability_example.py` for the full implementation.

## Contents
- `code/` — Scripts and notebooks
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization
- `interview_qa.md` — Interview Q&A 