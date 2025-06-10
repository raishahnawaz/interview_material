"""
Monitoring & Explainability Example: Drift Detection, Logging, SHAP, LIME
This script demonstrates basic model monitoring and explainability for a scikit-learn classifier on the Iris dataset.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import shap
from lime.lime_tabular import LimeTabularExplainer

# --- 1. Data Loading & Model Training ---
data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# --- 2. Monitoring: Drift Detection (Simple Example) ---
# Simulate drift by shuffling test data
X_test_drifted = X_test.sample(frac=1.0, random_state=1).reset_index(drop=True)
y_test_drifted = y_test.sample(frac=1.0, random_state=1).reset_index(drop=True)

orig_acc = accuracy_score(y_test, model.predict(X_test))
drifted_acc = accuracy_score(y_test_drifted, model.predict(X_test_drifted))
print(f"Original Test Accuracy: {orig_acc:.4f}")
print(f"Drifted Test Accuracy: {drifted_acc:.4f}")

# Log predictions for monitoring
preds = model.predict(X_test)
pd.DataFrame({"true": y_test, "pred": preds}).to_csv("prediction_log.csv", index=False)
print("Predictions logged to prediction_log.csv")

# --- 3. Explainability: SHAP ---
print("\nSHAP Explanation for a Test Sample:")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.initjs()
shap.summary_plot(shap_values, X_test, show=False)
plt.savefig("shap_summary.png")
print("SHAP summary plot saved as shap_summary.png")

# --- 4. Explainability: LIME ---
print("\nLIME Explanation for a Test Sample:")
explainer_lime = LimeTabularExplainer(X_train.values, feature_names=X_train.columns, class_names=data.target_names, discretize_continuous=True)
i = 0
exp = explainer_lime.explain_instance(X_test.values[i], model.predict_proba, num_features=4)
exp.save_to_file("lime_explanation.html")
print("LIME explanation saved as lime_explanation.html")

print("\nMonitoring and explainability demo complete.") 