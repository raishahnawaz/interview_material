# Machine Learning Interview Preparation: Project Index & User Guide

Welcome! This project is a hands-on, interview-focused resource for AI Engineer / Data Scientist roles, covering modern ML, NLP, LLMs, deployment, monitoring, explainability, and MLOps.

---

## Project Structure

- `use_case_*/` — Self-contained use cases (code, Dockerfile, requirements, docs)
- `docs/` — Unified architecture and ecosystem documentation
- `index.md` — This guide

## Use Cases
1. **Tabular ML**: scikit-learn, TensorFlow, PyTorch (Iris dataset)
2. **NLP Text Classification**: spaCy, HuggingFace Transformers (AG News)
3. **LLM Fine-tuning**: HuggingFace Transformers (IMDb)
4. **NLP Summarization**: T5 (CNN/DailyMail)
5. **Model Deployment**: FastAPI, Docker, Kubernetes, cloud
6. **Monitoring & Explainability**: Drift detection, SHAP, LIME
7. **MLOps**: DVC, MLflow, CI/CD, model registry
8. **(Planned) Vision & Time Series**: Image classification, forecasting

## How to Use
- Each use case has a `README.md` with setup, code, and interview Q&A.
- All use cases are containerized (see each `Dockerfile`).
- Unified docs in `docs/` explain the overall architecture and workflow.
- Run tests, demos, and reports as described in each use case.

## Quick Start
1. Clone the repo
2. Pick a use case folder and follow its `README.md`
3. Use the top-level `README.md` and this guide for navigation

## Further Resources
- See architecture docs in `docs/` for ecosystem overview and code mapping
- Use the interview Q&A in each use case for preparation
- Explore advanced topics (MLOps, monitoring, cloud, security) as needed

---

**Good luck with your interviews and ML projects!** 