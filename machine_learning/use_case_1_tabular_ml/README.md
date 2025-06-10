# Use Case 1: Tabular Machine Learning (Classification/Regression)

This use case demonstrates a typical tabular data ML workflow using scikit-learn, TensorFlow, and PyTorch. It covers:

- Data preprocessing and feature engineering
- Model training and evaluation
- Comparison of frameworks
- Containerized setup for reproducibility

## Workflow
1. **Data Loading & Preprocessing**: Loads the Iris dataset, splits into train/test, and scales features.
2. **Model Training**:
   - **scikit-learn**: RandomForestClassifier for baseline performance.
   - **TensorFlow**: Simple DNN for classification.
   - **PyTorch**: Feedforward neural network for classification.
3. **Evaluation**: Accuracy is reported for each framework.

## Code Highlights
- Each framework uses the same preprocessed data for fair comparison.
- Minimal, interview-ready code with clear comments.
- Easily extensible to other tabular datasets or models.

## Practical Tips
- Use `StandardScaler` for feature scaling in tabular ML.
- Compare classical ML (RandomForest) with deep learning (DNN/NN) for small datasets.
- Use Docker for reproducibility: `docker build -t tabular-ml . && docker run -it tabular-ml`.

## Visualization & Reporting
- An interactive Streamlit demo is provided in `code/streamlit_demo.py`.
- To run the demo:
  ```bash
  pip install streamlit
  streamlit run code/streamlit_demo.py
  ```

- To generate an HTML report of model results:
  ```bash
  python code/html_report.py
  # Output: iris_model_report.html
  ```

---
See `code/tabular_ml_example.py` for the full implementation.

## Contents
- `code/` — Scripts and notebooks
- `requirements.txt` — Python dependencies
- `Dockerfile` — Containerization
- `interview_qa.md` — Interview Q&A 