# Model Registry Example: MLflow Model Registry

This example demonstrates how to use MLflow Model Registry to manage and promote models.

---

## 1. Log a Model to MLflow
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
# ... train model ...
with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model", registered_model_name="IrisClassifier")
```

## 2. View and Manage Models
- Start the MLflow UI:
  ```bash
  mlflow ui
  ```
- Go to the "Models" tab to view registered models, versions, and stages (Staging, Production, Archived).

## 3. Transition Model Stages
- Use the MLflow UI or Python API to promote models:
```python
from mlflow.tracking import MlflowClient
client = MlflowClient()
client.transition_model_version_stage(
    name="IrisClassifier",
    version=1,
    stage="Production"
)
```

---

This workflow enables model versioning, stage transitions, and production-ready model management. 