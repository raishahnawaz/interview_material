
# Advanced Optimization Techniques in Spark & Delta Lake

## 1. Handle Data Skew with Salting

### 💡 What is Data Skew?
When doing joins or aggregations in distributed systems (like Spark), data skew happens when **some keys are much more frequent than others**. This causes **one partition to do more work**, leading to slow performance.

### 🧠 Real-Life Analogy
Imagine a queue with 10 counters. If 90% of people go to **counter 1**, that counter will be slow while the others are free. That’s skew!

### 📈 Use Case
You have a `transactions` table with a column `country_code`, and **most records have `country_code = 'US'`**. When joining on `country_code`, the US data causes one task to be overloaded.

### 🛠️ Solution: Salting the Join Key
We **add a random salt value** (e.g., a number from 0–9) to **spread** the skewed values across multiple partitions.

### ✅ Example (PySpark)
#### Original Join (Skewed)
```python
transactions = spark.read.parquet("/data/transactions")
countries = spark.read.parquet("/data/countries")

# Skewed join
joined = transactions.join(countries, on="country_code")
```

#### Optimized with Salting
```python
from pyspark.sql.functions import col, concat_ws, lit, rand, floor
from pyspark.sql.functions import explode, array

# Add salt to the skewed table
salted_transactions = transactions.withColumn("salt", floor(rand(seed=42) * 10)) \
                                  .withColumn("salted_country_code", concat_ws("_", col("country_code"), col("salt")))

# Expand small table with salt values
countries_with_salt = countries.withColumn("salt", explode(array([lit(i) for i in range(10)]))) \
                               .withColumn("salted_country_code", concat_ws("_", col("country_code"), col("salt")))

# Join on salted key
joined = salted_transactions.join(countries_with_salt, on="salted_country_code")
```

### 🎯 When to Use
- Joins involving skewed keys
- GroupBy / Aggregations on skewed data

---

## 2. Z-Order Clustering (Delta Lake Only)

### 💡 What is Z-Ordering?
**Z-ordering** is a technique to **physically rearrange** data files on disk based on the values of one or more columns. This improves **query performance** when you frequently filter on those columns.

### 🧠 Real-Life Analogy
Think of Z-order like **organizing books in a library**. If you often search by **author and genre**, you group books physically by author-genre, so searches are faster.

### 📈 Use Case
You often query a Delta Lake table like:
```sql
SELECT * FROM events WHERE device_id = 'abc123' AND event_date = '2025-06-01'
```
Z-ordering by `device_id` and `event_date` makes Spark **read fewer files**, improving speed.

### ✅ Example (Delta Lake, Databricks or PySpark with Delta)
```python
# Load or write your Delta Lake table
events.write.format("delta").save("/delta/events")

# Optimize the Delta table using Z-order
spark.sql("""
  OPTIMIZE delta.`/delta/events`
  ZORDER BY (device_id, event_date)
""")
```

### 🛠️ How it Helps
- Reduces the number of files read during filtering (pruning)
- Speeds up queries on those Z-ordered columns

### 🎯 When to Use
- Your queries often filter by the same 1–3 columns
- You have large Delta tables
- Use with **OPTIMIZE** command periodically

---

## ✅ Summary Table

| Technique             | Problem Solved           | Use Case Example                     | Tools Needed     |
|----------------------|---------------------------|--------------------------------------|------------------|
| **Salting**          | Data Skew in Joins        | Join on column with 90% same value   | Spark            |
| **Z-Ordering**       | Slow filter query due to scattered data | Filter on device_id, date, etc.      | Delta Lake + OPTIMIZE |
