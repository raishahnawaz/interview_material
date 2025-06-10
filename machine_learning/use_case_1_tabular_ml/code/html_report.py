import joblib
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# Load data and model
iris = load_iris()
X, y = iris.data, iris.target
try:
    model = joblib.load("iris_model.joblib")
except:
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    joblib.dump(model, "iris_model.joblib")

# Evaluate
preds = model.predict(X)
acc = accuracy_score(y, preds)
importances = model.feature_importances_
features = iris.feature_names

# Generate HTML report
html = f"""
<html>
<head><title>Iris Model Report</title></head>
<body>
<h1>Iris Model Report</h1>
<p><b>Accuracy:</b> {acc:.4f}</p>
<h2>Feature Importances</h2>
<ul>
"""
for feat, imp in zip(features, importances):
    html += f"<li>{feat}: {imp:.3f}</li>"
html += "</ul>\n</body>\n</html>"

with open("iris_model_report.html", "w") as f:
    f.write(html)

print("Report saved as iris_model_report.html") 