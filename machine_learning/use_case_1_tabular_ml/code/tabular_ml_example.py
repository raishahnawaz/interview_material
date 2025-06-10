"""
Tabular ML Example: Classification with scikit-learn, TensorFlow, and PyTorch
This script demonstrates data loading, preprocessing, model training, and evaluation using the Iris dataset.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

# --- 1. Data Loading & Preprocessing ---

data = load_iris()
X = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data loaded and preprocessed.")

# --- 2. scikit-learn Model ---
print("\n--- scikit-learn: RandomForestClassifier ---")
sk_model = RandomForestClassifier(random_state=42)
sk_model.fit(X_train_scaled, y_train)
sk_preds = sk_model.predict(X_test_scaled)
sk_acc = accuracy_score(y_test, sk_preds)
print(f"scikit-learn Accuracy: {sk_acc:.4f}")

# --- 3. TensorFlow Model ---
print("\n--- TensorFlow: Simple DNN ---")
import tensorflow as tf

tf_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train_scaled.shape[1],)),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])
tf_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
tf_model.fit(X_train_scaled, y_train, epochs=30, batch_size=8, verbose=0)
tf_loss, tf_acc = tf_model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"TensorFlow Accuracy: {tf_acc:.4f}")

# --- 4. PyTorch Model ---
print("\n--- PyTorch: Simple Feedforward NN ---")
import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class SimpleNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 16)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(16, output_dim)
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Prepare data for PyTorch
X_train_torch = torch.tensor(X_train_scaled, dtype=torch.float32).to(device)
y_train_torch = torch.tensor(y_train.values, dtype=torch.long).to(device)
X_test_torch = torch.tensor(X_test_scaled, dtype=torch.float32).to(device)
y_test_torch = torch.tensor(y_test.values, dtype=torch.long).to(device)

model = SimpleNN(X_train_scaled.shape[1], 3).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(50):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train_torch)
    loss = criterion(outputs, y_train_torch)
    loss.backward()
    optimizer.step()

# Evaluation
model.eval()
with torch.no_grad():
    outputs = model(X_test_torch)
    _, predicted = torch.max(outputs, 1)
    pt_acc = (predicted == y_test_torch).float().mean().item()
print(f"PyTorch Accuracy: {pt_acc:.4f}")

print("\nAll models trained and evaluated on the Iris dataset.") 