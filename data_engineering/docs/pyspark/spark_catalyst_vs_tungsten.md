
# 🔄 Catalyst vs Tungsten in Apache Spark

| Feature | Catalyst | Tungsten |
|--------|----------|----------|
| Purpose | Query optimization | Physical execution optimization |
| Focus | Logical and physical plan optimization | CPU, memory, and I/O performance |
| Type | Rule-based and cost-based engine | Low-level performance engine |
| Techniques | Predicate pushdown, plan rewriting | Off-heap memory, code generation |
| Affects | SQL, DataFrame, Dataset planning | Execution engine performance |
| Strength | Smart query planning | Speed and resource efficiency |

## Summary

- **Catalyst** handles the **planning** stage: transforming and optimizing queries.
- **Tungsten** handles the **execution** stage: speeding up the actual computation.
- Together, they power Spark SQL with both **smart planning** and **fast execution**.
