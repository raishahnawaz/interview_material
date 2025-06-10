"""
Vision Classification Example: PyTorch, MNIST
This script demonstrates image classification on MNIST with a simple CNN.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np

# --- 1. Data Loading ---
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
train_dataset = datasets.MNIST('.', train=True, download=True, transform=transform)
test_dataset = datasets.MNIST('.', train=False, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=1000, shuffle=False)

# --- 2. Model Definition ---
class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, 1)
        self.conv2 = nn.Conv2d(16, 32, 3, 1)
        self.fc1 = nn.Linear(32*5*5, 64)
        self.fc2 = nn.Linear(64, 10)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2)
    def forward(self, x):
        x = self.relu(self.conv1(x))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 32*5*5)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = SimpleCNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# --- 3. Training ---
print("Training...")
model.train()
for epoch in range(2):  # 2 epochs for demo
    total_loss = 0
    for data, target in train_loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(train_loader):.4f}")

# --- 4. Evaluation ---
print("Evaluating...")
model.eval()
correct = 0
total = 0
all_preds = []
all_imgs = []
with torch.no_grad():
    for data, target in test_loader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        preds = output.argmax(dim=1)
        correct += (preds == target).sum().item()
        total += target.size(0)
        all_preds.extend(preds.cpu().numpy())
        all_imgs.extend(data.cpu().numpy())
acc = correct / total
print(f"Test Accuracy: {acc:.4f}")

# --- 5. Visualization ---
print("Visualizing predictions...")
fig, axes = plt.subplots(2, 5, figsize=(10, 5))
for i, ax in enumerate(axes.flat):
    img = all_imgs[i][0]
    ax.imshow(img, cmap='gray')
    ax.set_title(f"Pred: {all_preds[i]}")
    ax.axis('off')
plt.tight_layout()
plt.savefig("mnist_predictions.png")
print("Sample predictions saved as mnist_predictions.png") 