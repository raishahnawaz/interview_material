
# ⚡ Snappy Compression

**Snappy** is a **fast and lightweight compression algorithm** developed by Google. It's designed to **prioritize speed over maximum compression ratio**, making it ideal for systems where performance is more critical than storage savings.

---

## 🔍 Key Features of Snappy

| Feature           | Description |
|-------------------|-------------|
| 💨 **Fast**       | Compresses and decompresses data at very high speeds (hundreds of MB/s) |
| 🔄 **Symmetric**  | Both compression and decompression are fast and efficient |
| 💾 **Moderate Compression** | Achieves 20–50% size reduction (not as small as gzip or bzip2) |
| ⚙️ **Lightweight**| Minimal CPU usage, great for real-time applications |
| 📦 **Block-based** | Works well on structured or chunked data formats (e.g., in Hadoop or Parquet) |

---

## 🧠 Use Cases

- **Big Data** frameworks (e.g., Apache Spark, Hadoop, Kafka)
- **Columnar storage** formats (e.g., Parquet, ORC)
- **Real-time streaming systems**
- **In-memory databases** (e.g., LevelDB, RocksDB)

---

## 📊 Comparison with Other Compression Algorithms

| Algorithm | Speed (✔ = fast) | Compression Ratio | Used In |
|----------|------------------|-------------------|---------|
| **Snappy** | ✔✔✔ | Moderate | Spark, Parquet, Kafka |
| Gzip      | ✔✔   | High     | Web, Logs, Files |
| Bzip2     | ✔     | Very High | Archiving |
| LZ4       | ✔✔✔   | Low–Moderate | Real-time data systems |

---

## ✅ Why Use Snappy in Spark or Kafka?

- Reduces I/O time without a big CPU cost  
- Keeps pipelines fast for large-scale data processing  
- Works well with columnar formats and distributed systems  
