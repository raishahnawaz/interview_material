# Monitoring & Explainability Interview Q&A

## General Questions

**Q: What is model drift and how can you detect it?**
A: Model drift occurs when the data distribution changes over time, reducing model performance. It can be detected by monitoring metrics (e.g., accuracy) or using statistical tests on input data.

**Q: Why is model explainability important?**
A: It helps build trust, supports debugging, ensures fairness, and is often required for regulatory compliance.

**Q: What are the differences between SHAP and LIME?**
A: SHAP provides global and local explanations based on Shapley values; LIME provides local explanations by perturbing input features.

## Code-Specific Questions

**Q: How does the code simulate drift?**
A: By shuffling the test data, it changes the input distribution, simulating drift and showing its impact on accuracy.

**Q: How are predictions logged for monitoring?**
A: Predictions and true labels are saved to a CSV file for later analysis.

**Q: How would you use SHAP and LIME in production?**
A: Use SHAP for regular feature importance monitoring and LIME for on-demand explanations of individual predictions. 