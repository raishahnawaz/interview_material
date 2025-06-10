
# 💬 Apache Spark Structured Streaming – Interview Questions & Answers

This document contains common interview questions for Apache Spark Structured Streaming, along with well-structured answers.

---

## 1. ❓ What is Structured Streaming in Spark?

**Answer:**  
Structured Streaming is a scalable and fault-tolerant stream processing engine built on the Spark SQL engine. It allows you to process real-time data as a continuously updating table using high-level declarative APIs.

- Uses the same DataFrame/Dataset API as batch processing
- Queries run continuously and update results incrementally
- Can run aggregations, joins, and windowed computations on streams

---

## 2. ❓ How does Structured Streaming differ from DStreams?

**Answer:**

| Feature             | DStreams                     | Structured Streaming         |
|---------------------|------------------------------|-------------------------------|
| API                 | RDD-based                    | DataFrame/Dataset-based      |
| Fault Tolerance     | Lineage-based                | Checkpointing + WAL          |
| Output Modes        | Limited                      | Append, Update, Complete     |
| State Management    | Manual                       | Built-in with watermarking   |
| Optimization        | Manual tuning                | Catalyst + AQE               |

---

## 3. ❓ What are the output modes in Structured Streaming?

**Answer:**

- **Append**: Only new rows are added (used for event logs).
- **Update**: Only rows that changed are updated (good for aggregates).
- **Complete**: Entire result is updated each trigger (used for global aggregates).

```python
.writeStream.outputMode("append|update|complete")
```

---

## 4. ❓ What are triggers in Structured Streaming?

**Answer:**

Triggers define when Spark processes new data:

- `Trigger.ProcessingTime("10 seconds")`: process every 10 seconds
- `Trigger.Once()`: process available data once and stop
- `Trigger.Continuous("1 second")`: low-latency continuous mode

---

## 5. ❓ How does Spark handle late data in Structured Streaming?

**Answer:**

Late data is handled using **watermarks**, which specify how long Spark should wait for late events.

```python
withWatermark("eventTime", "10 minutes")
```

This means Spark will wait up to 10 minutes for late data before considering it dropped.

---

## 6. ❓ How does fault tolerance work in Structured Streaming?

**Answer:**

- Uses **checkpointing** and **Write Ahead Logs (WAL)** for recovery
- If a node crashes, Spark reuses checkpointed state to resume processing
- State is stored in fault-tolerant storage like HDFS, S3, or DBFS

---

## 7. ❓ Can Structured Streaming do joins?

**Answer:**

Yes, it supports:
- Stream-Static Join: Stream joins with a batch dataset
- Stream-Stream Join: Two streaming sources join (requires watermarking)

```python
streaming_df.join(static_df, "id")
```

Stream-stream joins need watermarks and time windows to control state size.

---

## 8. ❓ What is watermarking in Spark?

**Answer:**

Watermarking defines the **maximum allowed delay** for data to be considered on-time.

- Helps Spark clean up state by evicting old data
- Prevents infinite state growth in joins and aggregations

---

## 9. ❓ How do you monitor and debug streaming jobs?

**Answer:**

- Use Spark UI → Structured Streaming tab
- Access `StreamingQuery` status via `.status` or `.lastProgress`
- Enable metrics and logs:
```python
query.awaitTermination()
query.status
query.lastProgress
```

---

## 10. ❓ What are the common sinks in Structured Streaming?

**Answer:**

- Console (for debugging)
- Memory (for temporary querying)
- File (CSV, Parquet, JSON)
- Kafka (via Kafka sink)
- Delta Lake / HDFS / S3 / JDBC

```python
.writeStream.format("parquet|delta|kafka|console")
```

---

## ✅ Summary

Apache Spark Structured Streaming allows for modern, low-latency, fault-tolerant streaming workloads using the same powerful Spark SQL APIs as batch processing. Mastering its features like output modes, triggers, watermarks, and joins is essential for building robust data pipelines.
