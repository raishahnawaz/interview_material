# 🧮 Join Row Count Comparison in BigQuery

This script demonstrates how different types of SQL joins (INNER, LEFT, RIGHT, FULL OUTER, and CROSS) behave when joining two small tables using BigQuery. It uses temporary tables with basic values, including a `NULL`, to show row count differences.

---

## ✅ Sample Data

**Tablex**

| x1   |
|------|
| 1    |
| 2    |
| 3    |
| NULL |

**Tabley**

| y1   |
|------|
| 1    |
| 1    |
| 2    |
| 3    |
| 5    |

---

## ✅ SQL Script (BigQuery)

```sql
-- Join Count Script for BigQuery using Sample Data
-- Demonstrates INNER, LEFT, RIGHT, FULL OUTER, and CROSS JOIN row counts

-- Step 1: Create temporary tables
CREATE TEMP TABLE Tablex (x1 INT64);
INSERT INTO Tablex (x1) VALUES (1), (2), (3), (NULL);

CREATE TEMP TABLE Tabley (y1 INT64);
INSERT INTO Tabley (y1) VALUES (1), (1), (2), (3), (5);

-- Step 2: Count rows for each JOIN type

-- INNER JOIN
SELECT COUNT(*) AS inner_join_count
FROM Tablex x
JOIN Tabley y ON x.x1 = y.y1;

-- LEFT JOIN
SELECT COUNT(*) AS left_join_count
FROM Tablex x
LEFT JOIN Tabley y ON x.x1 = y.y1;

-- RIGHT JOIN (use LEFT JOIN with swapped tables in BigQuery)
SELECT COUNT(*) AS right_join_count
FROM Tabley y
LEFT JOIN Tablex x ON x.x1 = y.y1;

-- FULL OUTER JOIN
SELECT COUNT(*) AS full_outer_join_count
FROM Tablex x
FULL OUTER JOIN Tabley y ON x.x1 = y.y1;

-- CROSS JOIN
SELECT COUNT(*) AS cross_join_count
FROM Tablex x
CROSS JOIN Tabley y;
```

---

## 📊 Expected Output

| Join Type         | Matching Logic          | Count | Notes                                                   |
|-------------------|--------------------------|--------|----------------------------------------------------------|
| **INNER JOIN**     | Only matched rows         | 5      | (1 joins 2×, 2 once, 3 once → 4 matched values, 5 rows)  |
| **LEFT JOIN**      | All from `x`, + matches   | 5      | Includes unmatched `NULL`                               |
| **RIGHT JOIN**     | All from `y`, + matches   | 6      | `5` unmatched → adds 1                                  |
| **FULL OUTER JOIN**| All from both + matches   | 7      | Combines unmatched from both tables                     |
| **CROSS JOIN**     | All combinations (x×y)    | 4×5=20 | Each row in `x` joins with all rows in `y`              |

---

## 📝 Notes

- `NULL` in `x1` does not match any value in join conditions.
- Duplicate values like `1` in Tabley generate multiple matches.
- CROSS JOIN creates Cartesian product (no ON clause required).
- BigQuery does not support native `RIGHT JOIN`, so it is emulated using `LEFT JOIN` on reversed tables.

---
