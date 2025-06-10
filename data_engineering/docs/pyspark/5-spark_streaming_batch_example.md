
# Spark Structured Streaming + Batch Job Example (For Absolute Beginners)

Apache Spark supports combining **streaming** and **batch** workloads using **Structured Streaming**, which treats real-time data as an unbounded table and integrates seamlessly with batch queries.

---

## 🎯 Goal

Build a Spark application that:
- Reads streaming data from a directory (new CSV files appearing every few seconds)
- Processes and aggregates that data in real-time
- Performs batch queries (e.g., finding top categories) on the streaming results

---

## 🧰 Prerequisites

- Apache Spark (3.x+)
- Scala or PySpark
- A directory for incoming files (used as streaming source)
- Basic knowledge of Python

---

## 📦 Step 1: Setup

Install PySpark (if not already):

```bash
pip install pyspark
```

Create a directory for incoming CSV files:

```bash
mkdir /tmp/stream_input
```

---

## 📑 Step 2: Code - PySpark Application

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window

# Step 1: Create SparkSession
spark = SparkSession.builder     .appName("Streaming + Batch Example")     .master("local[*]")     .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Step 2: Define streaming DataFrame
schema = "category STRING, amount DOUBLE, timestamp TIMESTAMP"

stream_df = spark.readStream     .schema(schema)     .option("header", "true")     .csv("/tmp/stream_input")  # Directory to watch

# Step 3: Streaming Aggregation
aggregated = stream_df.groupBy(
    window(col("timestamp"), "10 seconds"),  # Time window
    col("category")
).sum("amount")

# Step 4: Write to in-memory table
query = aggregated.writeStream     .outputMode("complete")     .format("memory")     .queryName("realtime_summary")     .start()

# Step 5: Batch Query over Streaming Output
import time
for i in range(5):
    time.sleep(10)
    print("Top Categories (last 10 seconds):")
    spark.sql("""
        SELECT category, SUM(sum(amount)) as total
        FROM realtime_summary
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """).show()

query.awaitTermination()
```

---

## 🧪 Step 3: Feed Data

Create CSV files and move them to `/tmp/stream_input/`:

Example CSV (save as `data1.csv`):
```csv
category,amount,timestamp
books,100.0,2025-06-10 10:01:01
electronics,200.0,2025-06-10 10:01:03
books,150.0,2025-06-10 10:01:08
```

Move the file:
```bash
mv data1.csv /tmp/stream_input/
```

Add more files every 10 seconds to simulate streaming.

---

## ⚙️ Configuration Notes

- `.outputMode("complete")`: replaces the entire result table every time.
- `.format("memory")`: stores results in temporary in-memory table for querying.
- `.queryName("realtime_summary")`: gives SQL access to the output.

---

## ✅ Summary

You’ve now created a **hybrid batch + streaming** Spark job:
- **Streaming Input**: Reads files as they arrive.
- **Real-Time Processing**: Aggregates over a time window.
- **Batch Query**: Uses SQL to query aggregated results from memory.

This model is extremely useful in:
- Real-time dashboards
- Fraud detection
- Time-based analytics
