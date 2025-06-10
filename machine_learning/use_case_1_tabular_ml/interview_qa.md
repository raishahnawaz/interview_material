# Tabular ML Interview Q&A

## General Questions

**Q: What are common preprocessing steps for tabular data?**
A: Handling missing values, encoding categorical variables, feature scaling (e.g., StandardScaler), and feature selection/engineering.

**Q: When would you use a RandomForest vs. a neural network?**
A: RandomForest is often better for small/medium tabular datasets with mixed feature types. Neural networks excel with large datasets and complex, non-linear relationships.

**Q: How do you prevent overfitting in tabular ML?**
A: Use cross-validation, regularization, early stopping (for NNs), and proper feature selection.

## Code-Specific Questions

**Q: Why is feature scaling important before training neural networks?**
A: Neural networks are sensitive to feature scale; scaling helps with convergence and stability.

**Q: How does the code ensure fair comparison between frameworks?**
A: All models use the same train/test split and scaled features.

**Q: How would you extend this code to a regression problem?**
A: Replace the classifier with a regressor (e.g., RandomForestRegressor, DNN with linear output) and use regression metrics (e.g., RMSE, MAE). 