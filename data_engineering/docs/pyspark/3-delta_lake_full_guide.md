
# 🔷 Delta Lake & Delta Tables Explained

Delta Lake is an **open-source storage layer** that adds powerful features like [**ACID transactions**](acid_properties_explained.md), **schema enforcement**, **time travel**, and **update/delete operations** on top of data lakes (e.g., S3, ADLS, GCS, HDFS).

---

## 📦 Is It a Database?

Delta Lake is **not a database** like PostgreSQL or MySQL. It's a **storage layer format** built on **Apache Parquet**, enhanced with:
- Transaction logs (`_delta_log/`)
- Support for updates, deletes, and merges
- Integration with Spark SQL and Databricks

You **query Delta Tables using Spark** or SQL on Databricks—not via JDBC/ODBC as in traditional databases.

---

## 🏗️ Architecture Overview

Delta Lake is composed of:

- ✅ **Parquet files** – the actual data
- 📝 **_delta_log/** – a transaction log that records every change
- 📦 **Delta Table** – a logical abstraction combining the above

![Delta Lake Architecture]()

---

## 🔄 Delta Tables and CDC (Change Data Capture)

Delta Tables **support incremental data** via:

### ✅ Upserts (MERGE):
You can merge new data (CDC) into a Delta table:

```python
spark.sql("""
MERGE INTO customers AS target
USING new_data AS source
ON target.customer_id = source.customer_id
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
```

This is perfect for **incremental loads** from streaming sources or CDC pipelines.

### 🕒 Time Travel:
Delta Lake keeps **historical versions**, allowing you to query older data:

```python
# View table as it was 3 versions ago
df = spark.read.format("delta").option("versionAsOf", 3).load("/delta/customers")
```

---

## 📈 When to Use Delta Lake

| Use Case                      | Delta Lake Feature               |
|------------------------------|----------------------------------|
| Incremental Loads / CDC      | MERGE INTO, UPSERT               |
| Frequent Schema Changes      | Schema Evolution                 |
| Data Correction (Deletes)    | DELETE, UPDATE                   |
| Audits / Time Travel         | Query by Version or Timestamp    |
| Query Speed Optimization     | Z-Ordering, File Compaction      |

---

## ✅ Summary

| Feature             | What It Does                                  |
|---------------------|-----------------------------------------------|
| ACID Transactions   | Guarantees consistency during reads/writes    |
| Schema Enforcement  | Ensures data types match schema               |
| Time Travel         | Lets you query older data versions            |
| Merge/Update/Delete | Full SQL-style DML support                    |
| Z-Ordering          | Optimizes file layout for fast queries        |

---

## 🛠️ Code Example: Create and Query Delta Table

```python
# Write to Delta Table
df.write.format("delta").save("/delta/events")

# Read it back
df2 = spark.read.format("delta").load("/delta/events")

# Update data
spark.sql("""
  UPDATE delta.`/delta/events`
  SET status = 'inactive'
  WHERE last_seen < '2025-01-01'
""")
```

---

## 📚 Learn More
- 🔗 [https://delta.io](https://delta.io) – Official Delta Lake site
- 📘 Ideal for building **reliable data lakes**, **lakehouses**, and **data pipelines**

---

# 🧊 Delta Lake vs Apache Iceberg vs Apache Hudi

Modern data lakes often face challenges such as lack of ACID transactions, inefficient updates, and no easy way to manage historical data. This is where modern **open table formats**—**Delta Lake**, **Apache Iceberg**, and **Apache Hudi**—come in.

---

## 📌 Common Features
All three formats provide:
- **ACID Transactions**
- **Schema Evolution**
- **Time Travel (Data Versioning)**
- **Efficient Data Updates/Deletes**
- **Streaming + Batch Support**
- **Cloud Storage Compatibility**

---

## 🔷 Delta Lake (by Databricks)

### ✅ Purpose
Adds ACID transactions and metadata management on top of Parquet. Best suited for Spark-based workflows and Databricks users.

### 📦 Use Cases
- Data warehousing on data lakes
- CDC for slowly changing dimensions (SCD)
- Machine Learning training sets with time travel
- Interactive data exploration

### 🧪 Real-World Code Example (PySpark)
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .getOrCreate()

df = spark.read.json("/data/new_users.json")
df.write.format("delta").mode("overwrite").save("/datalake/users")

# Update
from delta.tables import DeltaTable
delta_table = DeltaTable.forPath(spark, "/datalake/users")
delta_table.update("country = 'USA'", {"country": "'United States'"})

# Time travel
historical_df = spark.read.format("delta").option("versionAsOf", 1).load("/datalake/users")
```

### 💡 Delta Tables
- A **Delta Table** is a versioned table backed by Parquet + transaction logs (`_delta_log`).
- Allows rollback, auditing, time travel.

### 🔁 CDC Support
Delta supports `MERGE`, `UPDATE`, `DELETE`—ideal for slowly changing dimensions (SCD Type 1/2).

---

## 🧊 Apache Iceberg (by Netflix)

### ✅ Purpose
Built for **massive datasets** and **multi-engine support**. Solves Hive’s limitations like inefficient partitioning and metadata handling.

### 📦 Use Cases
- Analytics across petabytes of data
- GDPR compliance (deletes)
- Cross-engine query federation (Trino, Presto, Flink)

### 🧪 Real-World Code Example (PySpark)
```python
spark.sql("CREATE TABLE iceberg_catalog.db.sales (id BIGINT, amount DOUBLE, ts TIMESTAMP) USING iceberg")
spark.sql("INSERT INTO iceberg_catalog.db.sales VALUES (1, 100.5, current_timestamp())")

# Time travel
spark.sql("SELECT * FROM iceberg_catalog.db.sales VERSION AS OF 1")
```

### 🔁 CDC Support
Supports full upserts and deletes with **MERGE INTO** in Spark/Flink.

---

## 🔥 Apache Hudi (by Uber)

### ✅ Purpose
Optimized for **streaming ingestion**, **upserts**, and **incremental queries**.

### 📦 Use Cases
- Kafka ingestion pipelines (real-time)
- CDC from databases (e.g., Debezium → Hudi)
- Merge-on-read (MOR) tables for fresh data access

### 🧪 Real-World Code Example (PySpark)
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("HudiExample") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .getOrCreate()

df = spark.read.json("/data/kafka_users.json")
df.write.format("hudi") \
    .option("hoodie.table.name", "users_hudi") \
    .option("hoodie.datasource.write.recordkey.field", "user_id") \
    .option("hoodie.datasource.write.precombine.field", "ts") \
    .mode("append") \
    .save("/hudi/users")
```

### 🔁 CDC Support
Hudi natively supports **incremental pull**, **upserts**, **hard deletes**, and **merge-on-read (MOR)**.

---

## 🧠 Rich Comparison

| Feature                        | Delta Lake           | Apache Iceberg       | Apache Hudi           |
|-------------------------------|----------------------|-----------------------|------------------------|
| ACID Transactions             | ✅ Yes               | ✅ Yes               | ✅ Yes                |
| Time Travel                   | ✅ Yes               | ✅ Yes               | ✅ Yes                |
| Schema Evolution              | ✅ Strong            | ✅ Full               | ✅ Partial             |
| Streaming Ingest              | ⚠️ Partial            | ⚠️ Growing            | ✅ Excellent           |
| Partition Evolution           | ❌ No                | ✅ Yes               | ✅ Limited             |
| Query Engines Supported       | Spark, Databricks    | Spark, Flink, Trino   | Spark, Flink, Hive     |
| CDC Support                   | ✅ Merge/Update/Delete | ✅ Merge/Update/Delete | ✅ Upsert, Incremental |
| Best For                      | Data warehousing     | Multi-engine lakes    | Real-time ingestion    |
| Metadata Layer                | Delta Log (_delta_log) | Manifest + Snapshot | Timeline + Log         |
| Performance @ Large Scale     | Good                 | Excellent             | Good                   |

---

## 💬 Interview Scenario Questions

### 1. **Case: You’re building a data lake that handles frequent upserts and needs to support analytics and ML. What would you choose?**
**Answer:** Hudi is ideal for frequent upserts with real-time ingestion. But if analytics and ML pipelines are Spark-based, Delta Lake may be better due to simple `MERGE INTO` and Databricks optimization.

---

### 2. **Case: Your company wants to run Flink + Trino on S3 with massive petabyte-scale datasets and evolving schema.**
**Answer:** Apache Iceberg is best suited as it supports multiple engines, has robust schema evolution and partitioning, and scales efficiently.

---

### 3. **Question: How does time travel work in Delta Lake?**
**Answer:** Delta Lake maintains a transaction log (`_delta_log`) that stores each change as a version. You can query old versions using `versionAsOf` or `timestampAsOf`.

```python
spark.read.format("delta").option("versionAsOf", 2).load("/delta/sales")
```

---

### 4. **Case: How would you implement GDPR compliance (right to be forgotten) in a data lake?**
**Answer:** Iceberg or Hudi both allow deleting records and compacting/rewriting files afterward. Delta Lake supports DELETE, but requires VACUUM to remove deleted files.

---

## ✅ Summary

- **Use Delta Lake** if you're heavily Spark/Databricks-based and need strong transactional semantics.
- **Use Apache Iceberg** if you need cross-platform (Flink, Trino, Spark) support with schema/partition evolution.
- **Use Apache Hudi** for real-time ingestion, upserts, and incremental data pipelines.

*Created with ❤️ to demystify Delta Lake for big data engineers.*
