# 🧮 GitHub Commit Activity – Missing Dates Analysis (Multiple Approaches in BIGQUERY)

This document outlines different ways to find missing commit dates in GitHub data from BigQuery. It includes:

- ✅ **Part A** – Simulated Missing Dates using `GENERATE_DATE_ARRAY`
- ✅ **Part B** – Pure SQL methods without date array generation:
  - a. Estimate missing date counts using window functions
  - b. Retrieve actual missing dates per user
  - c. Filter users with missing dates in a custom range

---

## 📂 Dataset

We use the following dataset:

```sql
bigquery-public-data.github_repos.commits
```

Relevant fields:
- `committer.name` as `user_id`
- `committer.date.seconds` (converted to `DATE`)


- (Problem:)
- (Given a table of GitHub commit data &#40;user_id, commit_date&#41;,)

## ✅ Part A -- Return the maximum number of consecutive days with at least one commit per day

- (for each user_id, along with the start and end date of that longest streak.)

- (Dataset: bigquery-public-data.github_repos.commits)

- (Fields used:)

- (committer.name AS user_id)
- (committer.date &#40;struct: {seconds, nanos}&#41; converted to DATE)

- Query:
```
WITH commits AS (
  SELECT
    committer.name AS user_id,
    DATE(TIMESTAMP_SECONDS(committer.date.seconds)) AS created_at_date
  FROM `bigquery-public-data.github_repos.commits`
  WHERE committer.name IS NOT NULL
  LIMIT 100000
),

distinct_dates AS (
  SELECT DISTINCT user_id, created_at_date
  FROM commits
),

with_ranks AS (
  SELECT
    user_id,
    created_at_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at_date) AS rn
  FROM distinct_dates
),

grouped_by_diff AS (
  SELECT
    user_id,
    created_at_date,
    DATE_SUB(created_at_date, INTERVAL rn DAY) AS date_diff_group
  FROM with_ranks
),

streaks AS (
  SELECT
    user_id,
    date_diff_group,
    MIN(created_at_date) AS streak_start,
    MAX(created_at_date) AS streak_end,
    COUNT(*) AS streak_length
  FROM grouped_by_diff
  GROUP BY user_id, date_diff_group
),

max_streaks AS (
  SELECT
    user_id,
    MAX(streak_length) AS max_streak
  FROM streaks
  GROUP BY user_id
)

SELECT
  s.user_id,
  s.streak_start,
  s.streak_end,
  s.streak_length AS max_streak
FROM streaks s
JOIN max_streaks m
  ON s.user_id = m.user_id AND s.streak_length = m.max_streak
ORDER BY s.streak_length DESC
LIMIT 50;
```

## ✅ Part B: Simulated Missing Dates Using `GENERATE_DATE_ARRAY`

```sql
WITH skip_days AS (
  SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 60 DAY) AS d UNION ALL
  SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 62 DAY) UNION ALL
  SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 65 DAY)
),

-- Step 2: Extract commits excluding specific dates
commits AS (
  SELECT
    committer.name AS user_id,
    DATE(TIMESTAMP_SECONDS(committer.date.seconds)) AS created_at_date
  FROM `bigquery-public-data.github_repos.commits`
  WHERE committer.name IS NOT NULL
    AND DATE(TIMESTAMP_SECONDS(committer.date.seconds)) BETWEEN DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND CURRENT_DATE()
    -- AND DATE(TIMESTAMP_SECONDS(committer.date.seconds)) NOT IN (
    --   SELECT null FROM skip_days
    -- )
  LIMIT 100000
),

-- Step 3: Generate full date range for last year
calendar_dates AS (
  SELECT d FROM UNNEST(GENERATE_DATE_ARRAY(
    DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR),
    CURRENT_DATE()
  )) AS d
),

-- Step 4: Distinct commit dates overall
commit_dates_overall AS (
  SELECT DISTINCT created_at_date FROM commits
),

-- Step 5a: Missing dates overall
missing_dates_overall AS (
  SELECT
    d AS missing_date
  FROM calendar_dates c
  LEFT JOIN commit_dates_overall cd ON c.d = cd.created_at_date
  WHERE cd.created_at_date IS NULL
),

-- Step 5b: Missing dates per user
user_dates AS (
  SELECT DISTINCT user_id FROM commits
),

user_date_grid AS (
  SELECT
    u.user_id,
    d.d AS calendar_date
  FROM user_dates u
  CROSS JOIN calendar_dates d
),

user_commit_dates AS (
  SELECT DISTINCT user_id, created_at_date FROM commits
),

missing_dates_per_user AS (
  SELECT
    g.user_id,
    g.calendar_date AS missing_date
  FROM user_date_grid g
  LEFT JOIN user_commit_dates c
    ON g.user_id = c.user_id AND g.calendar_date = c.created_at_date
  WHERE c.created_at_date IS NULL
),

--let x=5
users_with_lessthan_x_missing_dates AS
(select count(*) as number_of_missing_dates, user_id from missing_dates_per_user
group by user_id
having count(*)<=150
)
-- -- Step 6a: Show missing dates overall
-- SELECT * FROM missing_dates_overall
-- ORDER BY missing_date
-- LIMIT 100;

-- Step 6b: Show missing dates per user
-- Optionally filter specific users



SELECT md.*,mdx.number_of_missing_dates FROM missing_dates_per_user md
inner join users_with_lessthan_x_missing_dates mdx on md.user_id=mdx.user_id
ORDER BY number_of_missing_dates,user_id, missing_date
LIMIT 100;
```

---

## ✅ Part C.1: Estimate Missing Date Counts (Window Method Only)

```sql
WITH commits AS (
  SELECT
    committer.name AS user_id,
    DATE(TIMESTAMP_SECONDS(committer.date.seconds)) AS created_at_date
  FROM `bigquery-public-data.github_repos.commits`
  WHERE committer.name IS NOT NULL
    AND DATE(TIMESTAMP_SECONDS(committer.date.seconds)) IS NOT NULL
  LIMIT 100000
),

ranked_commits AS (
  SELECT
    user_id,
    created_at_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at_date) AS rn
  FROM (
    SELECT DISTINCT user_id, created_at_date FROM commits
  )
),

diffs AS (
  SELECT
    user_id,
    created_at_date,
    DATE_SUB(created_at_date, INTERVAL rn DAY) AS diff_key
  FROM ranked_commits
),

streaks AS (
  SELECT
    user_id,
    MIN(created_at_date) AS streak_start,
    MAX(created_at_date) AS streak_end,
    COUNT(*) AS streak_length
  FROM diffs
  GROUP BY user_id, diff_key
),

commit_days_count AS (
  SELECT user_id, COUNT(DISTINCT created_at_date) AS commit_days
  FROM commits
  GROUP BY user_id
),

date_span_per_user AS (
  SELECT user_id,
         DATE_DIFF(MAX(created_at_date), MIN(created_at_date), DAY) + 1 AS total_days
  FROM commits
  GROUP BY user_id
),

missing_days_estimated AS (
  SELECT
    d.user_id,
    total_days,
    commit_days,
    total_days - commit_days AS missing_days_estimate
  FROM date_span_per_user d
  JOIN commit_days_count c ON d.user_id = c.user_id
)

SELECT * FROM missing_days_estimated
WHERE total_days < 10
ORDER BY missing_days_estimate DESC
LIMIT 100;
```

---

## ✅ Part C.2: Actual Missing Dates Per User (No `GENERATE_DATE_ARRAY`)

```sql
WITH commits AS (
  SELECT
    committer.name AS user_id,
    DATE(TIMESTAMP_SECONDS(committer.date.seconds)) AS created_at_date
  FROM `bigquery-public-data.github_repos.commits`
  WHERE committer.name IS NOT NULL
    AND DATE(TIMESTAMP_SECONDS(committer.date.seconds)) IS NOT NULL
  LIMIT 100000
),

ranked_commits AS (
  SELECT
    user_id,
    created_at_date,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at_date) AS rn
  FROM (
    SELECT DISTINCT user_id, created_at_date FROM commits
  )
),

diff_keyed AS (
  SELECT
    user_id,
    created_at_date,
    DATE_SUB(created_at_date, INTERVAL rn DAY) AS diff_key
  FROM ranked_commits
),

streaks AS (
  SELECT
    user_id,
    MIN(created_at_date) AS streak_start,
    MAX(created_at_date) AS streak_end
  FROM diff_keyed
  GROUP BY user_id, diff_key
),

user_commit_dates AS (
  SELECT DISTINCT user_id, created_at_date FROM commits
),

user_spans AS (
  SELECT user_id, MIN(created_at_date) AS min_date, MAX(created_at_date) AS max_date
  FROM user_commit_dates
  GROUP BY user_id
),

calendar_candidates AS (
  SELECT a.user_id, b.created_at_date AS calendar_date
  FROM user_spans a
  JOIN user_commit_dates b
    ON a.user_id = b.user_id
   AND b.created_at_date BETWEEN a.min_date AND a.max_date
),

missing_dates_per_user AS (
  SELECT
    c.user_id,
    c.calendar_date AS missing_date
  FROM calendar_candidates c
  LEFT JOIN commits d
    ON c.user_id = d.user_id AND c.calendar_date = d.created_at_date
  WHERE d.created_at_date IS NULL
),

filtered_users AS (
  SELECT user_id
  FROM missing_dates_per_user
  GROUP BY user_id
  HAVING COUNT(*) BETWEEN 10 AND 20
)

SELECT md.user_id, md.missing_date
FROM missing_dates_per_user md
JOIN filtered_users f ON md.user_id = f.user_id
ORDER BY md.user_id, md.missing_date
LIMIT 100;
```

---

## 📊 Summary of Approaches

| Approach             | Uses Date Generation? | Returns Actual Dates? | Filters Users? | Notes                            |
|----------------------|------------------------|------------------------|----------------|----------------------------------|
| Part A               | ✅ Yes (`GENERATE_DATE_ARRAY`) | ✅ Yes             | ❌ No          | Easy but uses static calendar   |
| Part B.1 (Estimate)  | ❌ No                  | ❌ No (counts only)     | ❌ No          | Lightweight estimate via window |
| Part B.2 (Actual)    | ❌ No                  | ✅ Yes                  | ✅ Yes         | Accurate with flexible filtering |

