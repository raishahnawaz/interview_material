# NLP Text Classification Interview Q&A

## General Questions

**Q: What are common approaches to text classification?**
A: Traditional ML (e.g., SVM, logistic regression with bag-of-words), deep learning (CNN/RNN), and transformer-based models (BERT, DistilBERT).

**Q: Why use pre-trained language models for NLP tasks?**
A: They capture rich language representations from large corpora, improving performance and reducing data requirements for downstream tasks.

**Q: How do you handle class imbalance in text classification?**
A: Use class weighting, resampling, or data augmentation techniques.

## Code-Specific Questions

**Q: Why use both spaCy and HuggingFace in this example?**
A: To compare traditional and transformer-based NLP pipelines and highlight their strengths.

**Q: How is the data split and used in both frameworks?**
A: The same train/test split is used for both, ensuring a fair comparison.

**Q: How would you adapt this code for binary sentiment analysis?**
A: Use a binary-labeled dataset (e.g., IMDb), adjust the number of labels, and update the model output layer accordingly. 