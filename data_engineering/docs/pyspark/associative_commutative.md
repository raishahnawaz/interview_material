# Associative vs Commutative Operations in Distributed Computing

Understanding the difference between **associative** and **commutative** operations is critical when working with distributed systems like Apache Spark.

---

## ✅ Associative Operations

An operation is **associative** if the grouping of operands does not affect the result.

### Example:

- **Addition**:  
  `(a + b) + c = a + (b + c)`

- **Multiplication**:  
  `(a * b) * c = a * (b * c)`

### Why Important?
Associativity allows intermediate results to be combined in **any order**, which is ideal for parallel processing.

---

## ✅ Commutative Operations

An operation is **commutative** if the order of operands does not affect the result.

### Example:

- **Addition**:  
  `a + b = b + a`

- **Multiplication**:  
  `a * b = b * a`

### Why Important?
Commutativity allows shuffling or reordering of values without impacting the correctness of results.

---

## ❌ Non-Associative Operations

These operations yield **different results** depending on how operands are grouped.

### Example:

- **Subtraction**:  
  `(10 - 5) - 2 = 3`, but `10 - (5 - 2) = 7`

- **Division**:  
  `(8 / 4) / 2 = 1`, but `8 / (4 / 2) = 4`

### In Spark:
Non-associative operations **can’t be reduced incrementally** (e.g., with `reduceByKey`). They require **full grouping of values** first (e.g., `groupByKey`).

---

## Summary Table

| Operation      | Associative | Commutative | Notes                          |
|----------------|-------------|-------------|--------------------------------|
| Addition (+)   | ✅ Yes      | ✅ Yes      | Ideal for parallel processing |
| Multiplication (*) | ✅ Yes  | ✅ Yes      | Ideal for parallel processing |
| Subtraction (-)| ❌ No       | ❌ No       | Must keep order & grouping    |
| Division (/)   | ❌ No       | ❌ No       | Must keep order & grouping    |

---

## 🧠 Tip for Spark:
Use `reduceByKey` only when operations are **associative** and preferably **commutative**.  
Use `groupByKey` for **non-associative** logic where you need access to all values.
