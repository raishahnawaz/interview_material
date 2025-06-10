# MLOps Example: DVC, MLflow, and Automation

This example demonstrates a simple MLOps workflow:
- Data and model versioning with DVC
- Experiment tracking with MLflow
- Automation with a Makefile

---

## 1. Data & Model Versioning with DVC

**Initialize DVC in your repo:**
```bash
dvc init
dvc add data/train.csv
git add data/train.csv.dvc .gitignore
git commit -m "Track training data with DVC"
```

**Track model artifacts:**
```bash
dvc add models/model.joblib
git add models/model.joblib.dvc
git commit -m "Track model artifact with DVC"
```

**Push data/model to remote storage:**
```bash
dvc remote add -d myremote <remote-url>
dvc push
```

---

## 2. Experiment Tracking with MLflow

**Log parameters, metrics, and artifacts in your training script:**
```python
import mlflow
import mlflow.sklearn

with mlflow.start_run():
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

**Start the MLflow UI:**
```bash
mlflow ui
```

---

## 3. Automation with Makefile

**Sample Makefile:**
```makefile
train:
	python train.py

track:
	mlflow ui

dvc_push:
	dvc push
```

---

This workflow ensures reproducibility, traceability, and automation in your ML projects. 