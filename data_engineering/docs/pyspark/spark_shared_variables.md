
# Spark Shared Variables Guide

Apache Spark provides two types of shared variables to support distributed computations where standard variable sharing across nodes is not possible: **Accumulators** and **Broadcast Variables**.

---

## 🔁 Accumulators

### 📌 What Are They?
Accumulators are **write-only shared variables** used for **aggregating information** from workers back to the driver.

- Executors can **only add** to accumulators.
- The **driver can read** the final value.
- Mainly used for **side-effect operations**, like monitoring or debugging.

---

### ✅ Use Cases

- Counting **corrupt/missing records**
- Logging metrics or monitoring execution
- Debugging large jobs without interrupting logic

---

### 🧪 Example (PySpark)

```python
from pyspark import SparkContext

sc = SparkContext("local", "Accumulator Example")

# Create an accumulator
error_count = sc.accumulator(0)

# Simulated data
data = ["record1", "bad_record", "record2", "bad_record"]

rdd = sc.parallelize(data)

def validate(record):
    if "bad" in record:
        error_count.add(1)
    return record

rdd.foreach(validate)

print("Number of bad records:", error_count.value)
```

---

### ⚠️ Caveats

- Accumulators are **not reliable** for driving logic.
- Spark may **re-run tasks**, causing double counting.
- Use **only for diagnostics**, not for computation results.

---

## 📦 Broadcast Variables

### 📌 What Are They?
Broadcast variables are **read-only variables** cached on all worker nodes, used to efficiently share **large, static datasets**.

- Avoid sending the same data with each task.
- Used typically for **lookup tables**, configs, or mappings.

---

### ✅ Use Cases

- Sharing **lookup dictionaries**
- Distributing **ML model weights or configs**
- Avoiding redundant data transfer in joins or maps

---

### 🧪 Example (PySpark)

```python
from pyspark import SparkContext

sc = SparkContext("local", "Broadcast Example")

# Large lookup dictionary
states = {"NY": "New York", "CA": "California", "TX": "Texas"}

# Broadcast it
broadcast_states = sc.broadcast(states)

# Sample data
data = ["NY", "TX", "CA", "FL"]
rdd = sc.parallelize(data)

def map_state(code):
    return broadcast_states.value.get(code, "Unknown")

mapped = rdd.map(map_state).collect()
print(mapped)  # Output: ['New York', 'Texas', 'California', 'Unknown']
```

---

### ⚠️ Notes

- Broadcast variables are **immutable** — update at driver and re-broadcast.
- Should be **small enough** to fit in executor memory.
- Ideal for **reference data**, not dynamic data.

---

## 🔄 Accumulator vs Broadcast Summary

| Feature                    | **Broadcast Variable**                             | **Accumulator**                               |
|----------------------------|----------------------------------------------------|------------------------------------------------|
| **Purpose**                | Share read-only data with all workers              | Aggregate data from workers to driver          |
| **Driver Can**             | Read & broadcast                                   | Create & read final value                      |
| **Workers Can**            | Only read                                          | Only add                                       |
| **Mutable?**               | No                                                 | Yes (increment only)                           |
| **Use in logic?**          | ✅ Yes                                             | ❌ No (not reliable)                           |
| **Examples**               | Lookup tables, config values                       | Error counters, missing record trackers        |

---

## 📌 Final Advice

- Use **broadcast** for large lookup datasets you need during transformations.
- Use **accumulators** for collecting counts/statistics that help **debug or monitor**, not for job control.

---
