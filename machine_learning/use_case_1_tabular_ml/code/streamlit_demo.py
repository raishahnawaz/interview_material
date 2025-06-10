import streamlit as st
import numpy as np
import pandas as pd
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

st.title("Iris Classifier Demo (RandomForest)")

# Load or train model
try:
    model = joblib.load("iris_model.joblib")
except:
    iris = load_iris()
    X, y = iris.data, iris.target
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    joblib.dump(model, "iris_model.joblib")

# User input
st.sidebar.header("Input Features")
def user_input():
    sepal_length = st.sidebar.slider('Sepal length', 4.0, 8.0, 5.1)
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.5, 3.5)
    petal_length = st.sidebar.slider('Petal length', 1.0, 7.0, 1.4)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    return np.array([[sepal_length, sepal_width, petal_length, petal_width]])

X_input = user_input()

# Prediction
pred = model.predict(X_input)[0]
proba = model.predict_proba(X_input)[0]
class_names = load_iris().target_names

st.write(f"### Predicted class: {class_names[pred]}")
st.write(f"Probabilities: {dict(zip(class_names, proba.round(2)))}")

# Feature importances
st.write("### Feature Importances:")
importances = model.feature_importances_
features = load_iris().feature_names
st.bar_chart(pd.Series(importances, index=features)) 