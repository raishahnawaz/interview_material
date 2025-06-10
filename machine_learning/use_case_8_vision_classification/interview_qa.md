# Vision Classification Interview Q&A

## General Questions

**Q: What are common architectures for image classification?**
A: Convolutional Neural Networks (CNNs) like LeNet, AlexNet, VGG, ResNet, EfficientNet.

**Q: Why use CNNs for images?**
A: CNNs exploit spatial structure, parameter sharing, and local connectivity, making them efficient and effective for images.

**Q: How do you prevent overfitting in vision models?**
A: Use data augmentation, dropout, regularization, and early stopping.

## Code-Specific Questions

**Q: How is the MNIST dataset loaded and preprocessed?**
A: Using torchvision's datasets and transforms for normalization and batching.

**Q: What is the model architecture in this example?**
A: A simple CNN with convolutional, ReLU, pooling, and fully connected layers.

**Q: How are predictions visualized?**
A: The code displays sample images with their predicted and true labels using matplotlib. 