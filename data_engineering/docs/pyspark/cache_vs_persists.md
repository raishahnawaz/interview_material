# 🧠 Understanding `cache()` and `persist()` in PySpark

In PySpark, transformations (like `.filter()`, `.map()`, `.join()`) are **lazy**, meaning they are **not executed immediately**. When you perform an **action** like `.count()` or `.show()`, Spark runs a job to compute the result.

If a DataFrame or RDD is used multiple times, Spark will **recompute it every time by default**, unless you **cache** or **persist** it.

---

## 🚀 What is `cache()`?

- `cache()` is a shorthand for:
  ```python
  df.persist(StorageLevel.MEMORY_AND_DISK)
  ```
- It **stores the DataFrame in memory** if there's enough RAM.
- If not, Spark will **spill it to disk**.

### ✅ Example

```python
df = spark.read.csv("big_dataset.csv")
df.cache()  # Cache it in memory

df.count()  # Triggers computation and caches result
df.show()   # Reuses cached result
```

---

## 🧊 What is `persist()`?

- `persist()` is more **flexible** than `cache()` — you can specify **storage levels**:
  - `MEMORY_ONLY`
  - `MEMORY_AND_DISK` (default)
  - `DISK_ONLY`
  - `MEMORY_ONLY_SER` (serialized)
  - And more...

### ✅ Example

```python
from pyspark.storagelevel import StorageLevel

df.persist(StorageLevel.DISK_ONLY)  # Persist only to disk
df.count()  # Triggers persistence
```

---

## 📌 When to Use `cache()` or `persist()`

Use them **when**:

- You are reusing a DataFrame **multiple times** in actions or stages.
- The computation is **expensive or time-consuming**.
- You want to **avoid recomputing** transformations.

---

## ⚠️ Be Careful: Unpersist When Done

Cached data **uses executor memory**, which is **limited**.  
Always `unpersist()` the DataFrame when it’s no longer needed.

```python
df.unpersist()
```

---

## 📊 Summary Table

| Method        | Storage Location         | Use When...                                      |
|---------------|---------------------------|--------------------------------------------------|
| `cache()`     | Memory, spill to disk     | Data is reused multiple times, fits in memory   |
| `persist()`   | Custom storage levels     | You want control over memory/disk storage       |
| `unpersist()` | —                         | To free up memory after data is no longer needed|

---

## 💡 Pro Tips

- Use `.cache()` for **quick optimization** if your data fits in memory.
- Use `.persist(level)` for **large or serialized** data handling.
- Monitor **Spark UI** to track memory/storage usage.
