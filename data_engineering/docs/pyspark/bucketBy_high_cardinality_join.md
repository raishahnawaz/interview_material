
# Understanding `bucketBy()` in Spark with High Cardinality Join Keys

## What is `bucketBy()`?

In Apache Spark, `bucketBy()` is a method used while writing DataFrames to a table. It organizes the data into a specified number of buckets based on the hash of one or more specified columns. This is particularly useful when you are working with join keys that have **high cardinality** (i.e., many unique values).

- **Partitions** the output files based on the **hash of one or more columns** (called "bucket columns")
- **Presorts** the data by those bucket columns
- Can be used to **optimize joins** between large DataFrames with the same bucketing scheme

## Why Use `bucketBy()` with High Cardinality Join Keys?

When performing joins in Spark on high cardinality keys, Spark typically performs **shuffle joins**, which can be expensive in terms of network I/O and execution time. Using `bucketBy()` can reduce the shuffle overhead during join operations by co-locating matching keys in the same bucket. This can lead to a significant **performance boost** for joins.


Joins in Spark often involve expensive **shuffling** of data across the cluster. This gets worse when:
- You join on **high-cardinality columns** (e.g., `user_id`, `session_id`)
- The datasets are **very large**


Using `bucketBy()`:
- Minimizes data movement
- Allows **Spark to use a more efficient join strategy**
- Results in **faster query performance**

## Sample Use Case: Optimizing Join with `bucketBy()`

Let's say we have two large datasets:
- `users` with a high-cardinality `user_id`
- `transactions` also keyed on `user_id`

### Step 1: Create Sample DataFrames

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import rand

spark = SparkSession.builder     .appName("BucketByExample")     .getOrCreate()

# Create users DataFrame
users = spark.range(1, 100001).withColumnRenamed("id", "user_id")

# Create transactions DataFrame with high-cardinality join key
transactions = users.sample(0.1).withColumnRenamed("user_id", "trans_user_id")
```

### Step 2: Save with Bucketing

```python
users.write     .bucketBy(100, "user_id")     .sortBy("user_id")     .mode("overwrite")     .saveAsTable("bucketed_users")

transactions.write     .bucketBy(100, "trans_user_id")     .sortBy("trans_user_id")     .mode("overwrite")     .saveAsTable("bucketed_transactions")
```

### Step 3: Perform Optimized Join

```python
bucketed_users = spark.table("bucketed_users")
bucketed_transactions = spark.table("bucketed_transactions")

# Join on user_id and trans_user_id
result = bucketed_users.join(
    bucketed_transactions,
    bucketed_users.user_id == bucketed_transactions.trans_user_id
)

result.show()
```

## Key Points
- Always use the same number of buckets and the same bucketing column(s) on both datasets to benefit from bucketing.
- Bucketing only works efficiently if you read the data from a bucketed table.
- Bucketing is especially useful when your join keys have **many unique values** (i.e., high cardinality).

## Summary

`bucketBy()` is a powerful technique to optimize joins in Spark when dealing with high cardinality keys. By pre-sorting and co-locating the data, Spark can reduce shuffle and improve performance.

---

**Note:** Bucketing is supported only when saving to tables (like Hive tables or Delta tables in Databricks), not when saving to Parquet or CSV directly.
