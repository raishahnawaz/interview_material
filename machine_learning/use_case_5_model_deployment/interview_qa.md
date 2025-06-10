# Model Deployment Interview Q&A

## General Questions

**Q: What are common ways to deploy ML models?**
A: REST APIs (FastAPI, Flask), batch jobs, streaming, serverless functions, and cloud ML platforms.

**Q: Why use FastAPI for model deployment?**
A: FastAPI is fast, easy to use, supports async, and provides automatic OpenAPI docs.

**Q: What are best practices for production ML APIs?**
A: Input validation, logging, monitoring, error handling, versioning, and security.

**Q: How do you secure a REST API?**
A: Use authentication (API keys, OAuth, JWT), HTTPS, rate limiting, and secrets management.

**Q: How do you handle privacy and PII in ML APIs?**
A: Avoid logging or exposing sensitive data, use encryption, and comply with regulations (e.g., GDPR, HIPAA).

**Q: How do you deploy an ML API to Kubernetes?**
A: Build and push a Docker image, create a Deployment and Service YAML, and apply them with `kubectl`. Use managed Kubernetes (EKS, GKE, AKS) for scaling.

**Q: What are options for cloud ML deployment?**
A: Use managed services like AWS SageMaker, GCP AI Platform, Azure ML, or serverless platforms like AWS Lambda, Google Cloud Run.

## Code-Specific Questions

**Q: How does the API validate input?**
A: Uses Pydantic models to enforce input types and structure.

**Q: How is the model loaded and used for prediction?**
A: The model is loaded from disk at startup and used in the `/predict` endpoint.

**Q: How is authentication implemented in the code?**
A: The `/predict` endpoint requires an API key in the `X-API-Key` header; unauthorized requests are rejected.

**Q: How would you extend this API to support multiple models?**
A: Add model selection logic, endpoints for different models, or a model registry. 