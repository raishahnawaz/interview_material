
# Apache Spark Join Strategies Explained

This document provides an in-depth explanation of the join strategies used in Apache Spark, including when to use each, how they perform in terms of time and space complexity, how they impact shuffling, and how they are handled by Spark's query planners, storage formats, and execution engine.

---

## 🔹 1. Broadcast Hash Join

### 📌 Description
Broadcasts the smaller table to all executors, allowing each to perform a local hash join.

### ✅ When to Use
- One table is small enough to fit in executor memory (default threshold: 10MB).
- Example: Joining a large sales fact table with a small product dimension.

### ⚙️ How Selected
```python
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 10 * 1024 * 1024)  # in bytes
```
- Set threshold to `-1` to disable auto-broadcast.
- Explicit in SQL: `/*+ BROADCAST(small_df) */`

### ⏱️ Time Complexity
- Lookup time: O(1) per row
- Broadcast cost: O(n) for small dataset

### 💾 Space Complexity
- Requires memory on each executor to store the broadcasted table.

### 🔄 Data Shuffling
- ❌ No shuffle needed

### 💽 Storage Compatibility
- Best with in-memory and small persistent tables (CSV, Parquet, Delta)

### 🧠 Catalyst & AQE
- Catalyst automatically rewrites joins to broadcast if size is under threshold.
- AQE can dynamically switch to broadcast join at runtime.

### ⚖️ Driver vs Executor Workload
- **Driver**: Evaluates table sizes and plans the broadcast.
- **Executors**: Receive and store full small table copy. Perform local joins.
- **Limitation**: Large broadcast tables may cause OOM on executors.

---

## 🔹 2. Shuffle Hash Join

### 📌 Description
Both datasets are shuffled based on the join key and hash tables are built in each partition.

### ✅ When to Use
- Medium-sized datasets that fit in memory.
- Broadcast is disabled or infeasible.

### ⚙️ How Selected
- Automatically selected if broadcast and sort-merge are not ideal.
- Not directly configurable but triggered by constraints and stats.

### ⏱️ Time Complexity
- Hashing + join: O(n + m) per partition

### 💾 Space Complexity
- Hash table memory required per partition

### 🔄 Data Shuffling
- ✅ Yes, shuffle both sides on join key

### 💽 Storage Compatibility
- Works on any format, e.g., Parquet, JSON, ORC

### 🧠 Catalyst & AQE
- Planner picks this when equi-join with hashable keys and memory available.
- AQE can adjust build/stream side.

### ⚖️ Driver vs Executor Workload
- **Driver**: Creates shuffle plan
- **Executors**: Shuffle and partition data, build local hash tables, perform joins
- **Constraints**: Can OOM if dataset is skewed or too large for memory

---

## 🔹 3. Sort Merge Join (SMJ)

### 📌 Description
Sorts both datasets on join key and merges using a merge-join algorithm.

### ✅ When to Use
- Large datasets that don’t fit in memory.
- Data is already sorted or partitioned on join keys.

### ⚙️ How Selected
```python
spark.conf.set("spark.sql.join.preferSortMergeJoin", True)
```
- Preferred over shuffle hash join when no side can be broadcasted.

### ⏱️ Time Complexity
- O(n log n) for sorting + O(n) for merging

### 💾 Space Complexity
- May spill to disk if sort overflows memory

### 🔄 Data Shuffling
- ✅ Required unless data is pre-sorted

### 💽 Storage Compatibility
- Optimized with sorted and range-partitioned Delta/Parquet tables

### 🧠 Catalyst & AQE
- Default strategy for large equi-joins
- AQE may downgrade to broadcast if small side detected

### ⚖️ Driver vs Executor Workload
- **Driver**: Coordinates shuffle, sort stages
- **Executors**: Perform sorting, merging
- **Constraints**: High disk I/O; needs sort buffer tuning

---

## 🔹 4. Bucketed or Partitioned Join

### 📌 Description
If both tables are pre-bucketed or partitioned on the join key, Spark can avoid shuffle.

### ✅ When to Use
- Tables written using identical bucket count and keys
- Efficient for static warehouse-style tables

### ⚙️ How Selected
```sql
-- Ensure both tables are bucketed:
CREATE TABLE fact_bucketed CLUSTERED BY (key) INTO 8 BUCKETS;
```
- Catalyst infers no shuffle if metadata matches

### ⏱️ Time Complexity
- O(n) per partition (no sort or hash)

### 💾 Space Complexity
- Minimal, just scanning and local merge

### 🔄 Data Shuffling
- ❌ None if bucketed/partitioned correctly

### 💽 Storage Compatibility
- Ideal for Delta, Hive, Parquet with bucketing

### 🧠 Catalyst & AQE
- Leverages catalog metadata
- AQE can fall back to shuffle join if mismatch found

### ⚖️ Driver vs Executor Workload
- **Driver**: Verifies bucketing metadata
- **Executors**: Local joins only, low CPU and memory
- **Constraints**: Requires identical bucketing and number of buckets

---

## 🔹 5. Cartesian Product (Cross Join)

### 📌 Description
Every row from one table is matched with every row from the other.

### ✅ When to Use
- No join key present.
- Manual cross-join required for matrix operations, testing.

### ⚙️ How Selected
```python
df1.crossJoin(df2)
```
- Must be explicitly invoked (not automatic)

### ⏱️ Time Complexity
- O(n × m)

### 💾 Space Complexity
- Extremely high — grows exponentially

### 🔄 Data Shuffling
- ✅ Always required unless using broadcast

### 💽 Storage Compatibility
- Any source format

### 🧠 Catalyst & AQE
- Must be explicit; AQE can’t optimize it much

### ⚖️ Driver vs Executor Workload
- **Driver**: Validates logic, prepares plan
- **Executors**: Heavy memory/CPU use
- **Constraints**: High failure risk for large datasets

---

## 📊 Strategy Comparison Summary

| Strategy              | Auto/Manual | Shuffle | Sort | Memory Use | When to Use                            | AQE Switchable |
|----------------------|-------------|---------|------|------------|----------------------------------------|----------------|
| Broadcast Hash Join  | Auto/manual | ❌ No   | ❌ No | Medium     | Small dim table joins                  | ✅ Yes         |
| Shuffle Hash Join    | Auto        | ✅ Yes  | ❌ No | High       | Medium data, not broadcastable         | ✅ Yes         |
| Sort Merge Join      | Auto        | ✅ Yes  | ✅ Yes| Medium     | Large equi-joins, sorted input         | ✅ Yes         |
| Bucketed Join        | Auto/manual | ❌ No   | ❌ No | Low        | Bucketed/partitioned big tables        | ✅ Yes         |
| Cartesian Join       | Manual      | ✅ Yes  | ❌ No | Very High  | No join keys, exhaustive pair matches  | ❌ No          |

---

## 🧠 Execution Flow: Driver vs Executor Role Comparison

| Component  | Broadcast Join         | Shuffle Hash Join       | Sort Merge Join          | Bucketed Join           | Cartesian Join         |
|------------|------------------------|--------------------------|---------------------------|--------------------------|-------------------------|
| **Driver** | Plans broadcast logic  | Plans shuffle, hash keys| Plans sort/shuffle       | Verifies metadata       | Plans full cross join   |
| **Executors** | Local join with copy  | Shuffle + hash join      | Shuffle + sort + merge   | Local join              | Heavy CPU & memory use |

### 🔧 Execution Constraints
- **Broadcast**: Executor OOM if size underestimated
- **Shuffle Hash**: Sensitive to skew; needs spill config
- **Sort Merge**: High disk usage; slow without tuning
- **Bucketed**: Needs strict alignment of bucket specs
- **Cartesian**: Extremely risky for large datasets

---

### 🔚 End of Document
