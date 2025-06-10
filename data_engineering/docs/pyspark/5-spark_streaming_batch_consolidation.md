
# 🔀 Spark Job with Combined Batch + Streaming Sources (with Consolidation)

This guide demonstrates how to build a Spark application that:
- Consumes **real-time streaming data** (e.g., new transaction logs from Kafka or files)
- Merges it with **historical batch data** (e.g., master product table from Parquet)
- Writes the **processed output** to a sink (Delta table or memory)
- Consolidates the results into a **target view or table** for unified analytics

---

## 🎯 Use Case

A company wants to:
1. Continuously stream sales data (from files or Kafka)
2. Combine it with a static product table (batch source)
3. Save per-product totals to a Delta table
4. Maintain a unified view combining all historical and live data

---

## 🛠️ Setup Requirements

- Apache Spark 3.x
- Delta Lake support (or write to memory if not available)
- Directory structure:

```
/data/products/      # Batch data (Parquet)
/data/stream_sales/  # Streaming data (CSV arriving continuously)
/data/output/        # Output consolidated
```

---

## 🧾 1. Sample Batch File (Parquet)

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder     .appName("Prepare Batch")     .getOrCreate()

product_df = spark.createDataFrame([
    (101, "Books"),
    (102, "Electronics"),
    (103, "Clothing")
], ["product_id", "category"])

product_df.write.mode("overwrite").parquet("/data/products/")
```

---

## 🧾 2. Streaming + Batch Join Logic

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window

spark = SparkSession.builder     .appName("Batch + Streaming Join")     .config("spark.sql.shuffle.partitions", "2")     .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Load batch source
products = spark.read.parquet("/data/products/")

# Define streaming source schema
schema = "sale_id INT, product_id INT, quantity INT, ts TIMESTAMP"

# Read streaming data from directory
sales_stream = spark.readStream     .schema(schema)     .option("header", "true")     .csv("/data/stream_sales/")

# Join streaming with batch
enriched_sales = sales_stream.join(products, on="product_id")

# Aggregated output by category
aggregated = enriched_sales.groupBy(
    window(col("ts"), "10 seconds"),
    col("category")
).sum("quantity").withColumnRenamed("sum(quantity)", "total_quantity")

# Write to Delta (or memory)
aggregated.writeStream     .outputMode("complete")     .format("memory")     .queryName("aggregated_stream")     .start()
```

---

## 🧾 3. Consolidated Batch Query (e.g., for Dashboard)

This reads from the real-time result and outputs a consolidated report every 30 seconds.

```python
import time

for _ in range(5):
    time.sleep(30)
    print("Live Dashboard - Total Sales Per Category:")
    spark.sql("""
        SELECT category, total_quantity
        FROM aggregated_stream
        ORDER BY total_quantity DESC
    """).show()
```

---

## 📥 4. Feeding the Stream

Use sample CSV files like:

```csv
sale_id,product_id,quantity,ts
1,101,2,2025-06-10 10:01:00
2,102,1,2025-06-10 10:01:03
3,101,3,2025-06-10 10:01:07
```

Add files to `/data/stream_sales/` every few seconds to simulate live streaming.

---

## 🧠 Explanation

| Component     | Role                                                                 |
|---------------|----------------------------------------------------------------------|
| Batch Source  | Static reference (e.g., product metadata)                           |
| Streaming     | Continuous input (new sales events)                                 |
| Join          | Enrich streaming data with product info                             |
| Output Sink   | Writes results to memory (can be replaced by Delta, Cassandra, etc.)|
| Consolidation | SQL query combines all output in a structured summary               |

---

## 🧪 Alternatives

- Replace file stream with Kafka: `readStream.format("kafka")...`
- Replace memory sink with Delta Lake, JDBC, Cassandra
- Use `.trigger(once=True)` for hybrid batch-once + stream

---

## ✅ Summary

This Spark job demonstrates:
- Hybrid ingestion (batch + stream)
- Real-time enrichment
- Consolidated analytics
