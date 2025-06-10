# MLOps Interview Q&A

## General Questions

**Q: What is MLOps and why is it important?**
A: MLOps (Machine Learning Operations) is the practice of automating and managing the ML lifecycle, including development, deployment, monitoring, and governance. It ensures reproducibility, scalability, and collaboration.

**Q: What are common tools for MLOps?**
A: DVC (data/model versioning), MLflow (experiment tracking), Kubeflow, Airflow, CI/CD tools (GitHub Actions, Jenkins), Docker, and cloud ML platforms.

**Q: How do you ensure reproducibility in ML projects?**
A: Use version control (Git), DVC for data/models, Docker for environments, and MLflow for experiment tracking.

## Code-Specific Questions

**Q: How does DVC help with data and model versioning?**
A: DVC tracks large files outside Git, enables reproducible pipelines, and supports remote storage.

**Q: How is MLflow used in the example?**
A: MLflow logs parameters, metrics, and models for each experiment, and provides a UI for comparison.

**Q: How would you extend this workflow for production?**
A: Add CI/CD pipelines for automated testing/deployment, use cloud storage for DVC, and integrate model monitoring. 