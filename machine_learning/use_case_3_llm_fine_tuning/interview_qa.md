# LLM Fine-tuning Interview Q&A

## General Questions

**Q: What is LLM fine-tuning and why is it important?**
A: Fine-tuning adapts a pre-trained large language model to a specific downstream task or domain, improving performance and relevance.

**Q: What are the main steps in fine-tuning a HuggingFace model?**
A: Prepare data, tokenize, set up the model and Trainer, train, and evaluate.

**Q: What are some challenges in LLM fine-tuning?**
A: Data quality, overfitting, compute requirements, and catastrophic forgetting.

## Code-Specific Questions

**Q: Why use DistilBERT for this example?**
A: DistilBERT is lightweight, fast, and suitable for demonstration and resource-limited environments.

**Q: How is the IMDb dataset prepared for fine-tuning?**
A: The script loads, splits, and tokenizes the data, then formats it for the Trainer API.

**Q: How would you adapt this code for multi-class classification?**
A: Change the number of labels, update the model output layer, and use a multi-class dataset. 