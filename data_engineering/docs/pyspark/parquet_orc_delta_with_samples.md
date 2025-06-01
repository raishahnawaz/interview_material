
# 📦 Why Use Parquet or ORC Instead of CSV/JSON?

## 🧾 Basic File Formats: CSV and JSON

### 📄 CSV (Row-Based, Text)
```
id,name,age
1,Alice,30
2,Bob,35
```

### 📄 JSON (Nested, Text)
```json
{"id": 1, "name": "Alice", "age": 30}
{"id": 2, "name": "Bob", "age": 35}
```

### ❌ Limitations
- Row-based → Read everything even if you need one column
- No compression
- No predicate pushdown or column pruning

---

## 📊 Columnar Formats: Parquet and ORC

These formats store **columns together** for fast access.

---

## 🧱 Sample File Structure: Parquet

**Data is organized into:**
- Row groups (set of rows)
- Column chunks (columns stored together)
- Pages (encoded and compressed data)
- Metadata (min/max values, null counts)

```
[Parquet File]
├── Row Group 1
│   ├── Column: id
│   ├── Column: name
│   └── Column: age
├── Row Group 2
│   ├── Column: id
│   ├── Column: name
│   └── Column: age
└── Footer Metadata
    ├── Schema
    ├── Compression info
    └── Column statistics (min, max, nulls)
```

---

## 🧱 Sample File Structure: ORC

**Data is organized into:**
- Stripes (similar to Parquet's row groups)
- Index data (min/max values for each stripe)
- Data section (actual column data)
- Footer (metadata and statistics)

```
[ORC File]
├── Stripe 1
│   ├── Index Data
│   └── Column Data
├── Stripe 2
│   ├── Index Data
│   └── Column Data
└── File Footer
    ├── Column Statistics
    └── File Metadata
```

---

## Benefits of Parquet/ORC Over CSV/JSON with Explanations

| Feature             | Parquet / ORC ✅ | CSV / JSON ❌ | Why Is This Available in Parquet / ORC But Not in CSV / JSON? |
|---------------------|------------------|----------------|----------------------------------------------------------------|
| **Column Pruning**     | Yes              | No             | Parquet/ORC store data column-wise, allowing Spark to read only required columns. CSV/JSON are row-based, so the whole row must be read. |
| **Predicate Pushdown** | Yes              | No             | Parquet/ORC store column-level statistics (min/max/null counts), enabling Spark to skip irrelevant data. CSV/JSON don’t store metadata. |
| **Compression**        | Built-in         | Limited        | Parquet/ORC support block-level compression and encoding (like RLE, Dictionary). CSV/JSON are just text and not optimized for compression. |
| **Parallel Reads**     | Yes              | Not optimal    | Columnar formats allow splits and multi-threaded reads. Row formats (CSV/JSON) have to be parsed line-by-line, slowing parallelism. |
| **[Schema Support](./schema_awareness_detailed.md)**     | Yes              | No             | Parquet/ORC embed full schemas and types. CSV has no types (everything is string); JSON is semi-structured but lacks strict typing. |

---

## 🧠 What is Predicate Pushdown?

Query:
```sql
SELECT name FROM people WHERE age > 30;
```

With **Parquet/ORC**:
- Skip reading rows where age ≤ 30 using metadata

With **CSV/JSON**:
- Load all rows, then apply the condition

---

## 📉 What is Column Pruning?

- If you only need the `name` column:
  - Parquet/ORC → Reads just the `name` column
  - CSV/JSON → Reads the whole row

---

## ✅ Recommended Usage

| Use Case                   | Recommended Format |
|----------------------------|--------------------|
| Analytical queries         | Parquet or ORC     |
| Human-readable config/logs | JSON               |
| Small, simple exports      | CSV                |

---

## 🏁 Summary

- Parquet and ORC are **optimized for big data**
- Store data in **compressed**, **columnar**, and **schema-aware** format
- Enable **faster queries** via **predicate pushdown** and **column pruning**

---

## 🧬 What About Delta Lake?

**Delta Lake** is an open-source storage layer that brings **ACID transactions** and **schema enforcement** to big data lakes.

It works **on top of Parquet files**, providing additional features like:

- **ACID transactions**
- **Time travel** (query older versions of your data)
- **Schema evolution**
- **Efficient upserts and deletes**

---

## 🧪 Using Delta Lake with PySpark and Blob Storage

### ✅ Recommended Setup

- **Storage**: Azure Blob Storage, AWS S3, GCS
- **Format**: Delta (internally uses Parquet)
- **API**: PySpark with Delta Lake

### 🔧 Writing Delta Tables

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder     .appName("DeltaExample")     .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")     .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")     .getOrCreate()

df = spark.read.json("path/to/json/files")

# Write as Delta format
df.write.format("delta").mode("overwrite").save("wasbs://container@storageaccount.blob.core.windows.net/delta/people")
```

### 🆕 Delta Table Structure (on Blob Storage)

```
[delta/people]
├── part-00000-*.snappy.parquet
├── ...
├── _delta_log/
│   ├── 00000000000000000000.json  ← transaction log files
│   ├── 00000000000000000001.json
│   └── ...
```

- Data stored as **Parquet**
- Metadata and transactions logged in `_delta_log`

---

## 🧠 Benefits of Delta Lake on Columnar Storage

| Feature             | Delta Lake          | Plain Parquet/ORC |
|---------------------|----------------------|-------------------|
| ACID transactions   | ✅ Yes               | ❌ No              |
| Time travel         | ✅ Yes               | ❌ No              |
| Schema enforcement  | ✅ Yes               | ❌ No              |
| Upserts & deletes   | ✅ Yes               | ❌ No (rewrite needed) |
| Blob compatibility  | ✅ Yes (Azure, S3)   | ✅ Yes             |

---

## 🏁 Summary: Why Delta + Parquet on Blob?

Delta Lake:
- Builds on **columnar speed** of Parquet
- Adds **robustness** for real-time and ETL pipelines
- Seamlessly integrates with **cloud blob storage**

Perfect for production-grade, scalable **data lakes**.

---

## 🧱 File Structure + Sample Data (Parquet vs ORC)

### 📦 Parquet Template + Sample

**File Structure:**
```
[Parquet File]
├── Row Group 1
│   ├── Column: id
│   ├── Column: name
│   └── Column: age
└── Footer Metadata
    ├── Schema
    ├── Compression info
    └── Column statistics (min, max, nulls)
```

**Sample Data Stored:**
```
Column: id   → [1, 2, 3]
Column: name → ["Alice", "Bob", "Carol"]
Column: age  → [30, 35, 40]
```

- Columns are stored together — efficient for queries like `SELECT name`.

---

### 📦 ORC Template + Sample

**File Structure:**
```
[ORC File]
├── Stripe 1
│   ├── Index Data
│   └── Column Data: id, name, age
└── File Footer
    ├── Column Statistics
    └── File Metadata
```

**Sample Data Stored:**
```
Column: id   → [1, 2, 3]
Column: name → ["Alice", "Bob", "Carol"]
Column: age  → [30, 35, 40]

Index Data:
- age: min=30, max=40
- id: min=1, max=3
```

- ORC keeps index stats per stripe for predicate pushdown and fast filtering.

---

## ✅ Usage Summary

Both **Parquet** and **ORC**:
- Store columnar data like `[1, 2, 3]` per column
- Enable compression and fast filtering
- Best for analytical queries at scale

