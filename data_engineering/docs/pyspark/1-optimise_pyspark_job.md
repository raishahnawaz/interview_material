# PySpark ETL Optimization Strategy

This document outlines a detailed and practical strategy to optimize PySpark ETL pipelines, including reasons and explanations behind each recommendation.

---

## 1. Code-Level Optimizations

### Use DataFrame API instead of RDDs
DataFrames are optimized internally using Spark's [Catalyst](./spark_catalyst.md) and [Tungsten](./spark_tungsten.md) engines, which allow for logical and physical plan optimizations. RDDs lack these optimizations and require manual management, making them slower and more error-prone for ETL.

### Avoid Python UDFs, prefer Spark SQL functions
Python UDFs serialize data between JVM and Python, introducing performance overhead and disabling Spark's internal optimizations. Use `pyspark.sql.functions` whenever possible to maintain Spark’s optimization capabilities.

### Use reduceByKey instead of groupByKey when working with RDDs
`reduceByKey` performs aggregation at the map side before shuffling the data, which reduces network I/O. In contrast, `groupByKey` shuffles all data first, leading to increased memory usage and slower performance.
[Detailed Comparison](./groupByKey_reduceByKey_combineByKey_comparison.md)

### Broadcast small lookup tables in joins
When joining a large table with a small one, use `broadcast()` on the small table. This prevents a full shuffle join by replicating the smaller table across all executors, drastically reducing network and disk I/O. [Constraints](./broadcast_join_limitations.md)

### Use cache() or persist() judiciously
If a DataFrame is reused in multiple stages or actions, caching it avoids recomputation and saves processing time. Be careful to unpersist when no longer needed to avoid unnecessary memory usage. [More insights](./cache_vs_persists.md)


### Select only required columns early
Use `.select()` to trim down unnecessary columns as early as possible. This reduces memory footprint and improves execution speed across transformations and actions.

### Push down filters using .filter() or .where()
Apply filtering logic as early as possible. Spark can push down filters to the data source level, which limits the amount of data loaded into memory, improving speed and efficiency.

---

## 2. Data Format and Storage Optimization

### Use columnar formats like Parquet or ORC instead of CSV/JSON
Parquet and ORC support column pruning and predicate pushdown, which are not available in CSV or JSON. These formats are compressed and optimized for analytical workloads, significantly improving I/O performance. [Details](./parquet_orc_delta_with_samples.md)

### Enable Snappy compression
Using  [Snappy compression](./snappy_compression_explained.md) with Parquet or ORC helps save storage and speeds up data reading due to reduced I/O, with minimal CPU overhead.

### Partition large datasets appropriately
Partitioning data by high-cardinality or frequently queried columns (e.g., date, region) enables Spark to skip reading entire partitions, improving query performance and reducing resource usage.

### Use bucketBy() on join keys with high cardinality
[Bucketing](./bucketBy_high_cardinality_join.md) pre-sorts data into files based on the hash of the specified columns. This reduces shuffle overhead during joins and enhances join performance.

### Avoid writing many small files
When writing data, avoid small file problems (which can cause high load on the driver and metadata servers) by using `.coalesce()` to reduce the number of partitions before writing.

### Optimize Cluster Utilization by Increasing Partitions on Large Clusters

When working with a large cluster and a DataFrame with few partitions, use `.repartition()` to increase parallelism and fully utilize available resources.

[Coalesce vs Repartition](./repartition_vs_coalesce.md)

---

## 3. Memory and Resource Tuning

### Configure executor memory and cores based on cluster size
Tuning `--executor-memory`, `--executor-cores`, and `--num-executors` ensures efficient use of cluster resources. Under-provisioning causes task spilling, while over-provisioning leads to executor failures.
[Details](./spark_executor_config_with_managers.md)

### Enable dynamic allocation
Dynamic allocation allows Spark to scale the number of executors based on workload, which improves resource utilization and lowers idle executor cost.

### Use broadcast joins for small tables
Broadcasting a small table in a join operation avoids the shuffle operation entirely, leading to faster and more efficient joins.

---

## 4. Job and DAG Optimization

### Avoid recomputation of DataFrames
Recomputing DataFrames in multiple stages increases job latency. Reuse by assigning intermediate results to variables or caching them if reused multiple times.

### Avoid unnecessary stages in the DAG
Combining transformations where possible reduces the number of shuffle boundaries and execution stages, which improves overall job execution time.

### Use coalesce() instead of repartition() when decreasing partitions
`coalesce()` merges partitions without a shuffle, making it much cheaper than `repartition()`, which causes a full shuffle. Use `coalesce()` to reduce partitions before writing data.

---

## 5. Partition Tuning and Parallelism

### Tune spark.sql.shuffle.partitions
The default value (typically 200) may not be optimal. Too many partitions add overhead, while too few cause skew. Tune this based on data volume and executor capacity.

### Enable Adaptive Query Execution (AQE)
AQE (available in Spark 3.0+) dynamically adjusts query plans during execution. It optimizes join strategies, handles skewed partitions, and modifies partition sizes to improve performance.

---

## 6. Monitoring and Debugging

### Use Spark UI for performance monitoring
Access the Spark UI to identify stage bottlenecks, task durations, shuffle sizes, and memory usage. It helps in diagnosing skewed tasks or expensive stages.

### Enable event logging for audit and tuning
Enable event logs to capture job execution details. These can be used for post-mortem analysis or tuning in continuous integration pipelines.

---

## 7. Best Practices Summary

- Use `coalesce()` after filtering to minimize the number of output files.
- Avoid Python UDFs to leverage Spark’s Catalyst optimizer.
- Use `broadcast()` for small tables in joins to avoid expensive shuffles.
- Reuse and cache frequently accessed DataFrames to reduce recomputation.
- Use `.select()` to pick only required columns early in the job.
- Apply `.filter()` early to reduce the data volume being processed.

---

## 8. Advanced Optimization Techniques [link](./advanced_optimization_techniques.md)

### Handle data skew with salting
If a join key is skewed (e.g., many rows with the same value), salting the key (adding a random prefix/suffix) distributes data more evenly across partitions, avoiding long-running tasks.

### Use Z-order clustering (Delta Lake only)
If using [Delta Lake](./delta_lake_full_guide.md), Z-ordering on frequently filtered columns improves query performance by co-locating related data on disk.

---

## Conclusion

This strategy provides a comprehensive approach to tuning PySpark ETL jobs. Apply these systematically based on the pipeline size, data characteristics, and cluster setup. Tailor individual components as needed for specific workloads.

For further assistance, provide a sample ETL job for targeted review and optimization.
