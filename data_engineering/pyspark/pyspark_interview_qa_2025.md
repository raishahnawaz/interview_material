
## PySpark Interview Questions and Answers (2025 Edition)

---

### 🔹 General Questions

1. **What is PySpark, and how does it work?**
   - PySpark is the Python API for Apache Spark. It allows Python developers to interface with Spark and use its distributed computing capabilities for big data processing. PySpark supports RDDs, DataFrames, and SQL APIs.

2. **Explain the architecture of PySpark.**
   - PySpark runs on top of Apache Spark, using a driver and multiple executors:
     - **Driver**: Orchestrates execution.
     - **Executors**: Run tasks in distributed fashion.
     - **Cluster Manager**: (YARN, Mesos, Standalone) handles resource allocation.

3. **Differences between RDD, DataFrame, and Dataset**:
   | Feature      | RDD             | DataFrame           | Dataset (Scala/Java) |
   |--------------|------------------|----------------------|-----------------------|
   | Type Safety | Yes             | No                   | Yes                   |
   | Performance | Low             | High (Catalyst)      | High                  |
   | Ease of Use | Low             | High                 | Moderate              |

4. **How does Spark handle fault tolerance?**
   - Through lineage information and DAG. If a partition fails, Spark re-computes lost data using the lineage.

5. **Transformations in PySpark:**
   - Lazy operations on RDDs/DataFrames, e.g., `map()`, `filter()`, `select()`, `groupBy()`.

6. **Narrow vs Wide Transformations:**
   - **Narrow**: Only one parent partition (e.g., `map`, `filter`).
   - **Wide**: Multiple parent partitions (e.g., `groupByKey`, `reduceByKey`). Triggers shuffling.

7. **Significance of DAG in Spark:**
   - DAG (Directed Acyclic Graph) represents the lineage of RDD transformations. Helps optimize execution plans.

8. **Driver vs Executor:**
   - **Driver**: Maintains the Spark context and schedules tasks.
   - **Executor**: Executes tasks and returns results to the driver.

9. **Schema Inference:**
   - Spark infers schema automatically from the data types in a DataFrame using reflection or user-provided schemas.

10. **Types of Joins in PySpark:**
   - `inner`, `left_outer`, `right_outer`, `full_outer`, `semi`, `anti`, and `cross` joins.

---

### ⚡ Performance Optimization Questions

11. **`cache()` vs `persist()`**
   - `cache()` = `persist(StorageLevel.MEMORY_AND_DISK)` (default).
   - `persist()` allows choosing different storage levels (e.g., disk-only).

12. **Broadcast joins:**
   - Used when one table is small. Reduces shuffling and speeds up joins.

13. **Spark job optimizations:**
   - Caching, partitioning, avoiding shuffles, broadcast joins, predicate pushdown, AQE.

14. **Benefits of Partitioning:**
   - Parallelism, reduced data movement, efficient I/O.

15. **`repartition()` vs `coalesce()`**
   - `repartition(n)` – increases partitions, full shuffle.
   - `coalesce(n)` – reduces partitions without full shuffle.

16. **Handling Skewed Data:**
   - Salting keys, broadcasting small table, custom partitioners.

17. **Lazy Evaluation:**
   - Transformations are lazy and only executed upon an action (like `count()`, `collect()`).

18. **Storage Levels:**
   - MEMORY_ONLY, MEMORY_AND_DISK, DISK_ONLY, OFF_HEAP, etc.

19. **Optimizing Joins:**
   - Use broadcast joins, filter before join, prefer `map-side` joins, ensure partition alignment.

20. **Adaptive Query Execution (AQE):**
   - Dynamically adjusts query plans at runtime for better optimization.

---

### 💻 PySpark Coding Questions

21. **Top 3 Most Occurring Words:**
```python
rdd = sc.textFile("file.txt")
rdd.flatMap(lambda x: x.split())\
   .map(lambda word: (word, 1))\
   .reduceByKey(lambda a, b: a + b)\
   .takeOrdered(3, key=lambda x: -x[1])
```

22. **Remove Duplicates:**
```python
df.dropDuplicates()
```

23. **Word Count:**
```python
rdd.flatMap(lambda x: x.split())\
   .map(lambda word: (word, 1))\
   .reduceByKey(lambda a, b: a + b)
```

24. **Group by and Average:**
```python
df.groupBy("department").agg(avg("salary"))
```

25. **Handle Nulls:**
```python
df.fillna(0)
df.dropna()
df.na.replace("NA", "Unknown")
```

26. **Count Distinct:**
```python
df.select(countDistinct("column_name"))
```

27. **Filter Records:**
```python
df.filter(df.salary > 50000)
```

28. **Read JSON:**
```python
df = spark.read.json("file.json")
```

29. **Second Highest Salary:**
```python
from pyspark.sql.window import Window
from pyspark.sql.functions import dense_rank

windowSpec = Window.orderBy(df["salary"].desc())
df.withColumn("rank", dense_rank().over(windowSpec))\
  .filter("rank = 2")
```

30. **Join DataFrames:**
```python
df1.join(df2, df1.id == df2.id).select(df1.name, df2.salary)
```

---

### 🧠 PySpark SQL Questions

31. **Create Temp View:**
```python
df.createOrReplaceTempView("employees")
```

32. **`select()` vs `withColumn()`**
   - `select()` returns a new DataFrame with selected columns.
   - `withColumn()` adds or replaces a column.

33. **Run SQL Queries:**
```python
spark.sql("SELECT * FROM employees WHERE salary > 50000")
```

34. **`explode()` vs `posexplode()`**
   - `explode()` – flattens array.
   - `posexplode()` – adds position index.

35. **Convert DataFrame to SQL Table:**
```python
df.write.saveAsTable("table_name")
```

36. **Window Functions:**
   - Examples: `row_number()`, `rank()`, `lead()`, `lag()` over partitions.

37. **RANK and DENSE_RANK:**
```python
from pyspark.sql.functions import rank, dense_rank
df.withColumn("rank", rank().over(windowSpec))
```

38. **Cumulative Sum:**
```python
from pyspark.sql.functions import sum
df.withColumn("cum_sum", sum("amount").over(Window.orderBy("date")))
```

39. **`groupBy()` vs `rollup()`:**
   - `groupBy()` aggregates at specific level.
   - `rollup()` adds sub-totals and grand totals.

40. **Pivot Operation:**
```python
df.groupBy("department").pivot("year").sum("revenue")
```

---

### 🔁 Streaming and Real-time

41. **What is Spark Streaming?**
   - Spark Streaming is a micro-batch streaming engine built on Spark Core. It processes live data streams using DStreams.

42. **Structured vs Unstructured Streaming:**
   - Structured: Tabular (DataFrame API, with schema).
   - Unstructured: DStream based, low-level.

43. **Handle Late Data:**
   - Use **event time** and **watermarking**.

44. **Watermarks:**
   - Used to track the progress of event-time and discard late data beyond a threshold.

---

### 📚 References & Resources
- [PySpark Official Docs](https://spark.apache.org/docs/latest/api/python/)
- [Cheat Sheet](https://databricks.com/p/resources/pyspark-cheat-sheet)
- [Awesome Spark GitHub](https://github.com/awesome-spark/awesome-spark)
- [MY OWN GUIDE](https://docs.google.com/document/d/17XWsX8aF8nTRhfCTJuTgSzqm3GPmC77PGFyu-DD83_4/edit?tab=t.0#heading=h.n7qvr4y4dpi)
---

### ✅ Badges
![PySpark](https://img.shields.io/badge/Apache_Spark-PySpark-orange)
![License](https://img.shields.io/badge/license-MIT-blue)
![Status](https://img.shields.io/badge/status-Ready--to--Use-brightgreen)
