# Use Case 8: Vision Classification (PyTorch, MNIST)

This use case demonstrates image classification using PyTorch on the MNIST handwritten digits dataset. It covers:

- Data loading and preprocessing
- Model training and evaluation
- Visualization of predictions
- Containerized setup for reproducibility

## Workflow
1. **Data Loading**: Downloads and preprocesses the MNIST dataset.
2. **Model Training**: Trains a simple CNN using PyTorch.
3. **Evaluation**: Reports accuracy and visualizes sample predictions.

## Code Highlights
- Uses PyTorch's DataLoader and torchvision for easy dataset handling.
- Minimal, interview-ready code with clear comments.
- Includes code for visualizing predictions.

## Practical Tips
- Use GPU if available for faster training.
- Experiment with deeper CNNs or data augmentation for better accuracy.
- Use Docker for reproducibility: `docker build -t vision-mnist . && docker run -it vision-mnist`.

---
See `code/vision_mnist_example.py` for the full implementation. 