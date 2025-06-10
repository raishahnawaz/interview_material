# NLP Summarization Interview Q&A

## General Questions

**Q: What is the difference between extractive and abstractive summarization?**
A: Extractive summarization selects sentences/phrases from the source text. Abstractive summarization generates new sentences, potentially rephrasing or condensing information.

**Q: What are common evaluation metrics for summarization?**
A: ROUGE, BLEU, METEOR, and human evaluation.

**Q: Why use transformer models for summarization?**
A: They capture long-range dependencies and can generate fluent, context-aware summaries.

## Code-Specific Questions

**Q: Why use T5 for this example?**
A: T5 is a versatile encoder-decoder model pre-trained for text-to-text tasks, including summarization.

**Q: How is the CNN/DailyMail dataset used in this code?**
A: The script loads articles and reference summaries, generates model summaries, and compares them.

**Q: How would you improve the evaluation in this code?**
A: Use ROUGE or BLEU for more robust, standard evaluation of summary quality. 