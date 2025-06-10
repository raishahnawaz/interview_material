# NLP Evaluation Metrics: A Beginner-Friendly Guide

This guide explains common evaluation metrics used in NLP, with examples and formulas where relevant.

---

## 1. Classification Metrics

- **Accuracy**: Proportion of correct predictions.
  - Formula: (TP + TN) / (TP + TN + FP + FN)
  - Example: 90 correct out of 100 → 90% accuracy.
- **Precision**: Proportion of positive predictions that are correct.
  - Formula: TP / (TP + FP)
  - Example: Of 10 spam emails flagged, 8 are actually spam → 80% precision.
- **Recall**: Proportion of actual positives that are found.
  - Formula: TP / (TP + FN)
  - Example: Of 12 actual spam emails, 8 are found → 66.7% recall.
- **F1 Score**: Harmonic mean of precision and recall.
  - Formula: 2 * (Precision * Recall) / (Precision + Recall)
- **Confusion Matrix**: Table showing counts of TP, TN, FP, FN.

---

## 2. Clustering Metrics

- **Adjusted Rand Index (ARI)**: Measures similarity between predicted and true clusters (adjusted for chance).
  - Range: -1 (bad) to 1 (perfect), 0 = random.
- **Silhouette Score**: Measures how similar an object is to its own cluster vs. other clusters.
  - Range: -1 (bad) to 1 (good).
- **Homogeneity, Completeness, V-Measure**: Assess how well clusters match true classes.

---

## 3. Topic Modeling Metrics

- **Coherence Score**: Measures interpretability of topics (how often top words co-occur).
  - Higher is better (usually 0–1).
- **Perplexity**: Measures how well a model predicts a sample (lower is better).
  - Used for LDA and language models.

---

## 4. Summarization Metrics

- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**:
  - Compares overlap of n-grams, word sequences, and word pairs between generated and reference summaries.
  - Common: ROUGE-1 (unigrams), ROUGE-2 (bigrams), ROUGE-L (longest common subsequence).
- **BLEU (Bilingual Evaluation Understudy)**:
  - Originally for translation, sometimes used for summarization.
  - Measures n-gram overlap, penalizes short outputs.

---

## 5. Translation Metrics

- **BLEU**: Measures n-gram overlap between machine and reference translations.
  - Range: 0 (bad) to 1 (perfect).
- **METEOR**: Considers synonyms and stemming, more flexible than BLEU.
- **TER (Translation Edit Rate)**: Number of edits needed to match reference.

---

## 6. Language Modeling Metrics

- **Perplexity**: Measures how well a model predicts a sequence (lower is better).
  - Formula: exp(-1/N * sum(log P(w_i)))
- **Cross-Entropy Loss**: Average negative log-likelihood of the true word.

---

## 7. Sequence Labeling Metrics

- **Token-level Accuracy**: Fraction of tokens labeled correctly.
- **Entity-level F1**: For NER, measures precision/recall of full entity spans.

---

## 8. Example Table: When to Use Which Metric

| Task                | Main Metrics         |
|---------------------|---------------------|
| Classification      | Accuracy, F1, Precision, Recall |
| Clustering          | ARI, Silhouette, V-Measure |
| Topic Modeling      | Coherence, Perplexity |
| Summarization       | ROUGE, BLEU         |
| Translation         | BLEU, METEOR, TER   |
| Language Modeling   | Perplexity, Cross-Entropy |
| Sequence Labeling   | Token Accuracy, F1   |

---

## 9. Further Reading
- [scikit-learn Metrics Documentation](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [ROUGE Paper](https://aclanthology.org/W04-1013/)
- [BLEU Paper](https://aclanthology.org/P02-1040/)
- [Topic Coherence in LDA](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 