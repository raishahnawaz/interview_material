
# ROW_NUMBER() vs RANK() vs DENSE_RANK() Cheat Sheet

## 📌 Overview Comparison

| Function         | Row Numbering Behavior        | Ties Handling                                   | Typical Use-Cases                                         |
|------------------|-------------------------------|--------------------------------------------------|-----------------------------------------------------------|
| `ROW_NUMBER()`   | Strictly sequential: `1, 2…`  | No ties — each row gets a **unique** value       | Pagination, deduplication, picking first row per group    |
| `RANK()`         | Gaps appear after ties: `1, 1, 3` | Tied rows share rank; **next rank is skipped**   | Podium ranking, ordinal positions with gaps               |
| `DENSE_RANK()`   | No gaps after ties: `1, 1, 2` | Tied rows share rank; **next rank is contiguous**| Leaderboards, percentile groups, compact rankings         |

---

## 🧪 Sample Query (BigQuery / SQL)

```sql
WITH scores AS (
  SELECT 'Alice' AS player, 98 AS pts UNION ALL
  SELECT 'Bob'  , 97 UNION ALL
  SELECT 'Cara' , 98 UNION ALL
  SELECT 'Dan'  , 94
)
SELECT
  player,
  pts,
  ROW_NUMBER()  OVER (ORDER BY pts DESC)       AS row_num,
  RANK()        OVER (ORDER BY pts DESC)       AS rnk,
  DENSE_RANK()  OVER (ORDER BY pts DESC)       AS dense_rnk
FROM scores;
```

🔍 Output

| player | pts | row_num | rnk | dense_rnk |
|--------|-----|---------|-----|-----------|
| Alice  | 98  | 1       | 1   | 1         |
| Cara   | 98  | 2       | 1   | 1         |
| Bob    | 97  | 3       | 3   | 2         |
| Dan    | 94  | 4       | 4   | 3         |

---

✅ **Choosing the Right Function**

| Question                                                    | Use              |
|-------------------------------------------------------------|------------------|
| Need a unique row number per row (e.g., pagination)?        | ROW_NUMBER()     |
| Want to show ordinal ranking, even if some ranks are skipped?| RANK()          |
| Want compact ranking with no gaps between tied rows?        | DENSE_RANK()     |

---

⚙️ **Common Patterns**

### 1️⃣ Keep latest record per key

```sql
SELECT * EXCEPT(row_num)
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts DESC) AS row_num
  FROM my_table
)
WHERE row_num = 1;
```

### 2️⃣ Leaderboard with ties (top 3)

```sql
SELECT *
FROM (
  SELECT player, pts,
         RANK() OVER (ORDER BY pts DESC) AS rnk
  FROM scores
)
WHERE rnk <= 3;
```

### 3️⃣ Revenue banding using DENSE_RANK

```sql
SELECT *,
       DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_band
FROM company_revenues;
```

---

🧠 **Summary**

- `ROW_NUMBER()`: Unique row number per row.
- `RANK()`: Ties share rank, skips following numbers.
- `DENSE_RANK()`: Ties share rank, no gaps afterward.

---

Let me know if you’d like a PDF version or syntax tailored to a specific SQL dialect (Postgres, SQL Server, etc.).
