# Use Case 5: Model Deployment (FastAPI)

This use case demonstrates deploying a trained ML/NLP model as a REST API using FastAPI. It covers:

- Packaging a trained model for inference
- Building a FastAPI REST API for serving predictions
- Containerized setup for reproducibility

## Workflow
1. **Model Training & Saving**: Trains a scikit-learn RandomForestClassifier on the Iris dataset and saves it with joblib (if not already present).
2. **API Setup**: Loads the model and defines a FastAPI app with a `/predict` endpoint.
3. **Prediction Endpoint**: Accepts feature input, runs inference, and returns the predicted class.

## Code Highlights
- Uses Pydantic for input validation and type safety.
- Demonstrates how to package and serve a model with minimal code.
- Easily extensible to other models or input schemas.

## Practical Tips
- Use Docker for reproducibility and easy deployment: `docker build -t iris-api . && docker run -p 8000:8000 iris-api`.
- For production, add logging, error handling, and model versioning.
- Use FastAPI's auto-generated docs at `/docs` for easy testing.

## Testing & Validation
- Unit tests are provided in the `tests/` folder using `pytest` and FastAPI's TestClient.
- To run tests:
  ```bash
  pip install pytest
  pytest tests/
  ```
- For test coverage, consider using `pytest-cov`.

## CI/CD
- A sample GitHub Actions workflow is provided in `.github/workflows/ci.yml`.
- It runs `pytest` on every push and pull request to the `main` branch for automated testing.

## Kubernetes & Cloud Deployment
- A sample Kubernetes deployment and service YAML is provided in `k8s_deployment.yaml`.
- To deploy on Kubernetes:
  ```bash
  kubectl apply -f k8s_deployment.yaml
  ```
- For cloud deployment:
  - Build and push your Docker image to a registry (e.g., Docker Hub, AWS ECR, GCP Artifact Registry).
  - Deploy using managed services (e.g., AWS EKS, GKE, Azure AKS) or serverless platforms (e.g., AWS Lambda with API Gateway, Google Cloud Run).
  - See [AWS SageMaker](https://aws.amazon.com/sagemaker/), [GCP AI Platform](https://cloud.google.com/ai-platform), or [Azure ML](https://azure.microsoft.com/en-us/services/machine-learning/) for managed ML deployment.

> **Note:** For cloud deployment, update the `image:` field in `k8s_deployment.yaml` to point to your container registry (e.g., `docker.io/youruser/iris-api:latest`).

## Visualization & Reporting
- For interactive model demos, consider using [Streamlit](https://streamlit.io/) or [Gradio](https://gradio.app/).
- For automated reporting, generate HTML or PDF reports from model results (see other use cases for examples).

---
See `code/main.py` for the full implementation.

## Contents
- `code/` — Scripts and app code
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization
- `interview_qa.md` — Interview Q&A 